# HTTP_test
## Описание работы программы
- Пример вывода статистики:
  - Host: https://google.com
  -   Success: 2
  -   Failed: 0
  -   Errors: 0
  -   Min: 0.7680274997837842
  -   Max: 0.8424048339948058
  -   Avg: 0.805216166889295
## Запуск программы
- python main.py -F hosts.txt -C 5
- python main.py -H https://ya.ru,https://google.com -C 5
- python main.py -H https://ya.ru -C 5 -O result.txt
## Установка
```bash
git clone https://github.com/IIWindigoo/HTTP_test.git
```
```bash
cd HTTP_test
```
```bash
pip install -r requirements.txt
```
