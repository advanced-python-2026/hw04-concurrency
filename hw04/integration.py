"""Задание 4.2 — Параллельный Monte Carlo для оценки числа pi.

Реализуйте:
- monte_carlo_pi(n_samples) — последовательная оценка pi
- monte_carlo_pi_parallel(n_samples, n_workers) — параллельная оценка pi
- compare_performance(samples_list) — сравнение производительности
"""

from __future__ import annotations


def monte_carlo_pi(n_samples: int) -> float:
    """Оценка числа pi методом Монте-Карло (последовательная версия).

    Генерирует n_samples случайных точек в единичном квадрате [0, 1) x [0, 1)
    и считает долю попавших в четверть единичного круга.

    Возвращает оценку pi.
    """
    # TODO: реализовать
    raise NotImplementedError


def monte_carlo_pi_parallel(n_samples: int, n_workers: int | None = None) -> float:
    """Оценка числа pi методом Монте-Карло (параллельная версия).

    Использует ProcessPoolExecutor для распределения работы между процессами.
    Каждый воркер обрабатывает n_samples // n_workers точек.

    Args:
        n_samples: общее количество точек
        n_workers: количество процессов (по умолчанию — число CPU)

    Возвращает оценку pi.
    """
    # TODO: реализовать
    raise NotImplementedError


def compare_performance(
    samples_list: list[int] | None = None,
) -> dict[int, dict[str, float]]:
    """Сравнить последовательную и параллельную версии.

    Args:
        samples_list: список значений n_samples для сравнения
            (по умолчанию [10**5, 10**6, 10**7])

    Возвращает словарь вида:
    {
        n_samples: {
            "sequential_time": float,
            "parallel_time": float,
            "sequential_pi": float,
            "parallel_pi": float,
            "speedup": float,
        }
    }
    """
    # TODO: реализовать
    raise NotImplementedError
