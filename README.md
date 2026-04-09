# ДЗ 4 — Многозадачность и синхронизация

Полный текст задания: https://advanced-python.ru/advanced-python/homework/hw04

## Быстрый старт

1. **Заполни `STUDENT.md`** — впиши ФИО точно как в ведомости (от этого зависит вариант).
2. **Установи зависимости:**
   ```bash
   uv sync
   ```
3. **Посмотри свой вариант:**
   ```bash
   uv run pytest -v --co
   ```
4. **Реализуй задания** в `hw04/fibonacci.py`, `hw04/integration.py` и `hw04/logger.py`.
5. **Проверь локально:**
   ```bash
   uv run ruff check .
   uv run ruff format --check .
   uv run pytest -v
   ```
6. **Запуш в main** — CI проверит автоматически.

## Структура

```
hw04/
  __init__.py        — пакет
  fibonacci.py       — сравнение подходов к параллелизму (задание 4.1)
  integration.py     — параллельный Monte Carlo (задание 4.2)
  logger.py          — ThreadedLogger с ротацией (задание 4.3)
tests/
  conftest.py        — определение варианта по ФИО
  test_fibonacci.py  — тесты параллельного вычисления Фибоначчи
  test_integration.py — тесты Monte Carlo
  test_logger.py     — тесты логгера с ротацией
```

## Задания

### 4.1 — Сравнение подходов к параллелизму (2 балла)

Вычислить `fib(35)` восемь раз четырьмя способами:
1. `threading.Thread`
2. `multiprocessing.Pool`
3. `concurrent.futures.ProcessPoolExecutor`
4. Sub-interpreters (`interpreters`, Python 3.13+)

Вывести таблицу сравнения с временем и ускорением.

### 4.2 — Параллельный Monte Carlo (2 балла)

Оценить число π методом Монте-Карло:
- Последовательная версия
- Параллельная версия с `ProcessPoolExecutor`
- Сравнить при `n_samples` = 10^5, 10^6, 10^7

### 4.3 — ThreadedLogger с ротацией (2 балла)

- N потоков-продюсеров генерируют лог-сообщения с уникальными ID
- 1 поток-консьюмер пишет в файл
- Ротация файла при достижении `max_lines`
- Корректное завершение через `stop()`
- Вариант определяет примитивы синхронизации
