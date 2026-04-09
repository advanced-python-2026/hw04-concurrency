"""Задание 4.1 — Сравнение подходов к параллелизму.

Вычислить fib(35) восемь раз четырьмя способами и сравнить производительность.

Реализуйте следующие функции:
- fib(n) — рекурсивное вычисление числа Фибоначчи
- run_threading(fn, args_list) — параллельное вычисление через threading.Thread
- run_multiprocessing_pool(fn, args_list) — через multiprocessing.Pool
- run_executor(fn, args_list) — через concurrent.futures.ProcessPoolExecutor
- run_interpreters(fn, args_list) — через sub-interpreters (Python 3.13+)
- compare_all(n, repeat) — запуск всех методов, возврат таблицы результатов
"""

from __future__ import annotations


def fib(n: int) -> int:
    """Рекурсивное вычисление числа Фибоначчи."""
    # TODO: реализовать
    raise NotImplementedError


def run_threading(fn, args_list: list) -> list:
    """Вычислить fn(*args) для каждого args в args_list через threading.Thread.

    Возвращает список результатов в том же порядке.
    """
    # TODO: реализовать
    raise NotImplementedError


def run_multiprocessing_pool(fn, args_list: list) -> list:
    """Вычислить fn(*args) для каждого args в args_list через multiprocessing.Pool.

    Возвращает список результатов в том же порядке.
    """
    # TODO: реализовать
    raise NotImplementedError


def run_executor(fn, args_list: list) -> list:
    """Вычислить fn(*args) для каждого args в args_list через ProcessPoolExecutor.

    Возвращает список результатов в том же порядке.
    """
    # TODO: реализовать
    raise NotImplementedError


def run_interpreters(fn, args_list: list) -> list:
    """Вычислить fn(*args) для каждого args в args_list через sub-interpreters.

    Возвращает список результатов в том же порядке.
    """
    # TODO: реализовать
    raise NotImplementedError


def compare_all(n: int = 35, repeat: int = 8) -> dict[str, dict]:
    """Запустить все методы и вернуть результаты сравнения.

    Возвращает словарь вида:
    {
        "method_name": {
            "results": [...],
            "time": float,       # секунды
            "speedup": float,    # относительно sequential
        }
    }

    Методы: "sequential", "threading", "multiprocessing", "executor", "interpreters"
    """
    # TODO: реализовать
    raise NotImplementedError
