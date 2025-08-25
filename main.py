from argparse import ArgumentParser
import requests
from time import perf_counter


parser = ArgumentParser(prog="HTTP_test")
parser.add_argument("-H", "--hosts", type=str, help="Адреса хостов")
parser.add_argument("-C", "--count", type=int, default=1, help="Количество запросов")

args = parser.parse_args()

print(args.hosts.split(","), args.count)

def test_host(host):
    try:
        start = perf_counter()
        response = requests.get(host, timeout=10)
        end = perf_counter()
        duration = end - start
        return response.status_code, duration
    except requests.exceptions.RequestException:
        return None, None

for host in args.hosts.split(","):
    success = 0
    failed = 0
    errors = 0
    dur_list = []

    for _ in range(args.count):
        s_code, duration = test_host(host)
        if s_code is None:
            errors += 1
            continue
        if 200 <= s_code <= 399:
            success += 1
        if 400 <= s_code <= 599:
            failed += 1
        dur_list.append(duration)

    print(f"Host: {host}\n"
            f"Success: {success}\n" 
            f"Failed: {failed}\n" 
            f"Min: {min(dur_list)}\n"
            f"Max: {max(dur_list)}\n" 
            f"Avg: {sum(dur_list) / len(dur_list)}\n")