from argparse import ArgumentParser
import requests
from time import perf_counter
import sys
import re


def test_host(host):
    """Запрос к серверу. Возвращает (status_code, duration) или (None, None) при ошибке"""
    try:
        start = perf_counter()
        response = requests.get(host, timeout=10)
        end = perf_counter()
        duration = end - start
        return response.status_code, duration
    except requests.exceptions.RequestException:
        return None, None

def work(host, count):
    """Выполнение нескольких запросов к хосту и возвращает статистику"""
    success = 0
    failed = 0
    errors = 0
    durations = []

    for _ in range(count):
        s_code, duration = test_host(host)
        if s_code is None:
            errors += 1
            continue
        if 200 <= s_code <= 399:
            success += 1
        if 400 <= s_code <= 599:
            failed += 1
        if duration is not None:
            durations.append(duration)
    
    return {
        "host": host,
        "success": success,
        "failed": failed,
        "errors": errors,
        "durations": durations
    }

def get_stats(stats):
    """Вывод статистики"""
    durations = stats["durations"]
    min_time = min(durations) if durations else "--"
    max_time = max(durations) if durations else "--"
    avg_time = sum(durations) / len(durations) if durations else "--"

    stats = (f"Host: {stats["host"]}\n"
          f"  Success: {stats["success"]}\n" 
          f"  Failed: {stats["failed"]}\n"
          f"  Errors: {stats["errors"]}\n" 
          f"  Min: {min_time}\n"
          f"  Max: {max_time}\n" 
          f"  Avg: {avg_time}\n")
    return stats

def validate_count(count):
    """Валидация --count"""
    if count <= 0:
        print("Ошибка: -C/--count должен быть положительным числом")
        sys.exit(1)
    return count

def validate_hosts(hosts):
    """Валидация --hosts"""
    url = re.compile(r"^https://[a-zA-Z0-9.-]+\.[a-z]{2,}(/.*)?$")
    for h in hosts:
        if not url.match(h):
            print("Ошибка: -H/--hosts принимает адреса в формате https://example.com")
            sys.exit(1)
    return hosts


if __name__ == "__main__":
    parser = ArgumentParser(prog="HTTP_test")
    parser.add_argument("-H", "--hosts", type=str, help="Адреса хостов")
    parser.add_argument("-C", "--count", type=int, default=1, help="Количество запросов")
    parser.add_argument("-F", "--file", type=str, help="Файл со списком адресов хостов")
    parser.add_argument("-O", "--output", type=str, help="Файл для сохранения результатов")

    args = parser.parse_args()
    if args.hosts and args.file:
        print("Ошибка: Одновременно может быть указан только один из ключей –F или -H")
        sys.exit(1)
    if args.hosts:
        hosts = args.hosts.split(",")
    elif args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                hosts = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Ошибка: файл {args.file} не найден")
            sys.exit(1)
    else:
        print("Ошибка: должен быть указан один из ключей -F или -H")
        sys.exit(1)

    hosts_after_validate = validate_hosts(hosts)
    count = validate_count(args.count)

    result = []
    for host in hosts_after_validate:
        stats_dict = work(host, count)
        stats_text = get_stats(stats_dict)
        result.append(stats_text)

        if not args.output:
            print(stats_text)

    if args.output:
        text = "\n".join(result)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)