"""Тесты задания 4.1 — Сравнение подходов к параллелизму."""

from __future__ import annotations

import os
import time

import pytest

from hw04.fibonacci import (
    compare_all,
    fib,
    run_executor,
    run_interpreters,
    run_multiprocessing_pool,
    run_threading,
)

FIB_35 = 9227465
N = 35
REPEAT = 8


class TestFib:
    """Тесты рекурсивной функции Фибоначчи."""

    def test_fib_base_cases(self):
        assert fib(0) == 0
        assert fib(1) == 1

    def test_fib_small_values(self):
        assert fib(10) == 55
        assert fib(20) == 6765

    def test_fib_35(self):
        """fib(35) должен вернуть 9227465."""
        result = fib(N)
        assert result == FIB_35


class TestRunMethods:
    """Тесты параллельных методов вычисления."""

    @pytest.fixture
    def args_list(self) -> list[tuple[int]]:
        return [(N,)] * REPEAT

    @pytest.fixture
    def sequential_results(self) -> list[int]:
        return [fib(N)] * REPEAT

    def test_threading_returns_correct_results(self, args_list, sequential_results):
        """threading.Thread возвращает правильные результаты."""
        results = run_threading(fib, args_list)
        assert results == sequential_results

    def test_threading_returns_list_of_eight(self, args_list):
        """threading возвращает список из 8 элементов."""
        results = run_threading(fib, args_list)
        assert len(results) == REPEAT
        assert all(r == FIB_35 for r in results)

    def test_multiprocessing_returns_correct_results(self, args_list, sequential_results):
        """multiprocessing.Pool возвращает правильные результаты."""
        results = run_multiprocessing_pool(fib, args_list)
        assert results == sequential_results

    def test_executor_returns_correct_results(self, args_list, sequential_results):
        """ProcessPoolExecutor возвращает правильные результаты."""
        results = run_executor(fib, args_list)
        assert results == sequential_results

    def test_all_methods_return_same_results(self, args_list):
        """Все методы возвращают одинаковые результаты."""
        threading_res = run_threading(fib, args_list)
        mp_res = run_multiprocessing_pool(fib, args_list)
        executor_res = run_executor(fib, args_list)
        expected = [FIB_35] * REPEAT

        assert threading_res == expected
        assert mp_res == expected
        assert executor_res == expected

    def test_results_are_list_of_eight_identical(self, args_list):
        """Результат — список из 8 одинаковых значений fib(35)."""
        for runner in (run_threading, run_multiprocessing_pool, run_executor):
            results = runner(fib, args_list)
            assert isinstance(results, list)
            assert len(results) == REPEAT
            assert len(set(results)) == 1
            assert results[0] == FIB_35


class TestRunInterpreters:
    """Тесты корректности run_interpreters."""

    def test_run_interpreters_returns_correct_results(self):
        """run_interpreters возвращает правильные значения fib."""
        args_list = [(N,)] * REPEAT
        results = run_interpreters(fib, args_list)
        assert results == [FIB_35] * REPEAT


@pytest.mark.skipif(
    os.environ.get("CI") == "true" or (os.cpu_count() is not None and os.cpu_count() < 2),
    reason="Speedup unreliable in CI / need multiple cores",
)
class TestSpeedup:
    """Тесты производительности параллельных методов."""

    @pytest.fixture
    def args_list(self) -> list[tuple[int]]:
        return [(N,)] * REPEAT

    def _time_sequential(self) -> float:
        start = time.perf_counter()
        for _ in range(REPEAT):
            fib(N)
        return time.perf_counter() - start

    def test_multiprocessing_faster_than_sequential(self, args_list):
        """multiprocessing.Pool быстрее последовательного выполнения (минимум 1.3x)."""
        seq_time = self._time_sequential()

        start = time.perf_counter()
        run_multiprocessing_pool(fib, args_list)
        mp_time = time.perf_counter() - start

        speedup = seq_time / mp_time
        assert speedup >= 1.3, (
            f"multiprocessing speedup {speedup:.2f}x < 1.3x "
            f"(sequential={seq_time:.3f}s, mp={mp_time:.3f}s)"
        )

    def test_executor_faster_than_sequential(self, args_list):
        """ProcessPoolExecutor быстрее последовательного выполнения."""
        seq_time = self._time_sequential()

        start = time.perf_counter()
        run_executor(fib, args_list)
        executor_time = time.perf_counter() - start

        speedup = seq_time / executor_time
        assert speedup >= 1.3, (
            f"executor speedup {speedup:.2f}x < 1.3x "
            f"(sequential={seq_time:.3f}s, executor={executor_time:.3f}s)"
        )


class TestCompareAll:
    """Тесты функции compare_all."""

    def test_compare_all_returns_all_methods(self):
        """compare_all возвращает результаты для всех методов."""
        results = compare_all(n=30, repeat=4)
        expected_methods = {
            "sequential",
            "threading",
            "multiprocessing",
            "executor",
            "interpreters",
        }
        assert set(results.keys()) == expected_methods

    def test_compare_all_structure(self):
        """Каждый метод содержит results, time, speedup."""
        results = compare_all(n=30, repeat=4)
        for method, data in results.items():
            assert "results" in data, f"{method}: missing 'results'"
            assert "time" in data, f"{method}: missing 'time'"
            assert "speedup" in data, f"{method}: missing 'speedup'"
            assert isinstance(data["results"], list), f"{method}: results is not a list"
            assert isinstance(data["time"], float), f"{method}: time is not float"
            assert isinstance(data["speedup"], float), f"{method}: speedup is not float"

    def test_compare_all_sequential_speedup_is_one(self):
        """Ускорение последовательного метода должно быть 1.0."""
        results = compare_all(n=30, repeat=4)
        assert results["sequential"]["speedup"] == pytest.approx(1.0)
