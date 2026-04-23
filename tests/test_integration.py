"""Тесты задания 4.2 — Параллельный Monte Carlo для оценки pi."""

from __future__ import annotations

import math
import os
import time

import pytest

from hw04.integration import (
    compare_performance,
    monte_carlo_pi,
    monte_carlo_pi_parallel,
)


class TestMonteCarloSequential:
    """Тесты последовательной версии Monte Carlo."""

    def test_returns_float(self):
        """Функция возвращает float."""
        result = monte_carlo_pi(1000)
        assert isinstance(result, float)

    def test_close_to_pi_small(self):
        """При n_samples=10^5 результат близок к pi (допуск 0.1)."""
        result = monte_carlo_pi(10**5)
        assert abs(result - math.pi) < 0.1, f"pi estimate {result} too far from {math.pi}"

    def test_close_to_pi_medium(self):
        """При n_samples=10^6 результат близок к pi (допуск 0.05)."""
        result = monte_carlo_pi(10**6)
        assert abs(result - math.pi) < 0.05, f"pi estimate {result} too far from {math.pi}"

    def test_reasonable_range(self):
        """Результат в разумных пределах [2.5, 3.8]."""
        result = monte_carlo_pi(10**4)
        assert 2.5 < result < 3.8, f"pi estimate {result} outside reasonable range"


class TestMonteCarloParallel:
    """Тесты параллельной версии Monte Carlo."""

    def test_returns_float(self):
        """Функция возвращает float."""
        result = monte_carlo_pi_parallel(1000)
        assert isinstance(result, float)

    def test_close_to_pi(self):
        """Параллельная версия возвращает значение близкое к pi."""
        result = monte_carlo_pi_parallel(10**6)
        assert abs(result - math.pi) < 0.05, f"parallel pi estimate {result} too far from {math.pi}"

    def test_similar_to_sequential(self):
        """Обе версии дают похожие результаты при одинаковом n_samples.

        Из-за случайности сравниваем с допуском 0.1.
        """
        n = 10**6
        seq = monte_carlo_pi(n)
        par = monte_carlo_pi_parallel(n)

        # Оба должны быть близки к pi, а значит и друг к другу
        assert abs(seq - math.pi) < 0.1
        assert abs(par - math.pi) < 0.1

    def test_accepts_n_workers(self):
        """Функция принимает параметр n_workers."""
        result = monte_carlo_pi_parallel(10**5, n_workers=2)
        assert isinstance(result, float)
        assert 2.5 < result < 3.8


@pytest.mark.skipif(
    os.cpu_count() is not None and os.cpu_count() < 2,
    reason="Need multiple cores",
)
class TestSpeedup:
    """Тесты производительности параллельной версии."""

    def test_parallel_faster_for_large_n(self):
        """Параллельная версия быстрее при n_samples=10^7 (минимум 1.3x)."""
        n = 10**7

        start = time.perf_counter()
        monte_carlo_pi(n)
        seq_time = time.perf_counter() - start

        start = time.perf_counter()
        monte_carlo_pi_parallel(n)
        par_time = time.perf_counter() - start

        speedup = seq_time / par_time
        assert speedup >= 1.3, (
            f"parallel speedup {speedup:.2f}x < 1.3x "
            f"(sequential={seq_time:.3f}s, parallel={par_time:.3f}s)"
        )


class TestAccuracy:
    """Тесты точности при увеличении числа выборок."""

    def test_higher_samples_better_accuracy(self):
        """Большее число выборок даёт лучшую точность."""
        errors = {}
        for n in [10**3, 10**5, 10**6]:
            estimate = monte_carlo_pi(n)
            errors[n] = abs(estimate - math.pi)

        # В среднем ошибка должна уменьшаться с ростом n
        # Допускаем, что 10^6 точнее 10^3
        assert errors[10**6] < errors[10**3], (
            f"Accuracy did not improve: "
            f"error@10^3={errors[10**3]:.5f}, error@10^6={errors[10**6]:.5f}"
        )


class TestComparePerformance:
    """Тесты функции compare_performance."""

    def test_returns_dict(self):
        """compare_performance возвращает словарь."""
        result = compare_performance([10**4, 10**5])
        assert isinstance(result, dict)
        assert 10**4 in result
        assert 10**5 in result

    def test_result_structure(self):
        """Каждая запись содержит нужные поля."""
        result = compare_performance([10**4])
        data = result[10**4]
        assert "sequential_time" in data
        assert "parallel_time" in data
        assert "sequential_pi" in data
        assert "parallel_pi" in data
        assert "speedup" in data

    @pytest.mark.slow
    def test_default_samples_list(self):
        """По умолчанию используется [10^5, 10^6, 10^7]."""
        result = compare_performance()
        assert 10**5 in result
        assert 10**6 in result
        assert 10**7 in result
