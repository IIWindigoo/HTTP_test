from argparse import ArgumentParser
import requests
from time import perf_counter


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

def print_stats(stats):
    """Вывод статистики"""
    durations = stats["durations"]
    min_time = min(durations) if durations else "--"
    max_time = max(durations) if durations else "--"
    avg_time = sum(durations) / len(durations) if durations else "--"

    print(f"Host: {stats["host"]}\n"
          f"  Success: {stats["success"]}\n" 
          f"  Failed: {stats["failed"]}\n"
          f"  Errors: {stats["errors"]}\n" 
          f"  Min: {min_time}\n"
          f"  Max: {max_time}\n" 
          f"  Avg: {avg_time}\n")

if __name__ == "__main__":
    parser = ArgumentParser(prog="HTTP_test")
    parser.add_argument("-H", "--hosts", type=str, help="Адреса хостов")
    parser.add_argument("-C", "--count", type=int, default=1, help="Количество запросов")

    args = parser.parse_args()
    hosts = args.hosts.split(",")

    for host in hosts:
        stats = work(host, args.count)
        print_stats(stats)