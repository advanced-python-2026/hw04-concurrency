"""Тесты задания 4.3 — ThreadedLogger с ротацией файлов."""

from __future__ import annotations

import re
import time

import pytest

from hw04.logger import ThreadedLogger


class TestLoggerBasic:
    """Базовые тесты логгера."""

    def test_creates_output_file(self, tmp_path):
        """Логгер создаёт файл лога."""
        log_file = tmp_path / "test.log"
        logger = ThreadedLogger(
            log_path=log_file,
            max_lines=1000,
            n_producers=2,
            messages_per_producer=5,
        )
        logger.start()
        logger.stop(timeout=10.0)

        assert log_file.exists(), "Log file was not created"

    def test_all_messages_written(self, tmp_path):
        """Все сообщения записаны — ни одно не потерялось."""
        log_file = tmp_path / "test.log"
        n_producers = 3
        messages_per_producer = 10
        expected_total = n_producers * messages_per_producer

        logger = ThreadedLogger(
            log_path=log_file,
            max_lines=1000,
            n_producers=n_producers,
            messages_per_producer=messages_per_producer,
        )
        logger.start()
        logger.stop(timeout=10.0)

        # Собираем строки из всех файлов (основной + ротированные)
        all_lines = _collect_all_lines(log_file)
        assert len(all_lines) == expected_total, (
            f"Expected {expected_total} messages, got {len(all_lines)}"
        )

    def test_no_duplicate_messages(self, tmp_path):
        """Нет дублирующихся сообщений."""
        log_file = tmp_path / "test.log"
        n_producers = 3
        messages_per_producer = 20

        logger = ThreadedLogger(
            log_path=log_file,
            max_lines=1000,
            n_producers=n_producers,
            messages_per_producer=messages_per_producer,
        )
        logger.start()
        logger.stop(timeout=10.0)

        all_lines = _collect_all_lines(log_file)
        assert len(all_lines) == len(set(all_lines)), "Duplicate messages found"

    def test_message_format_includes_producer_id(self, tmp_path):
        """Каждое сообщение содержит ID продюсера."""
        log_file = tmp_path / "test.log"
        n_producers = 3
        messages_per_producer = 5

        logger = ThreadedLogger(
            log_path=log_file,
            max_lines=1000,
            n_producers=n_producers,
            messages_per_producer=messages_per_producer,
        )
        logger.start()
        logger.stop(timeout=10.0)

        all_lines = _collect_all_lines(log_file)
        assert len(all_lines) > 0, "No messages written"

        # Каждая строка должна содержать идентификатор продюсера
        producer_ids_found = set()
        for line in all_lines:
            # Ожидаем формат с ID продюсера в квадратных скобках или в начале строки
            match = re.search(r"^\[(\d+)\]", line)
            assert match, f"No producer ID found in line: {line}"
            producer_ids_found.add(int(match.group(1)))

        # Должны быть сообщения от всех продюсеров
        assert len(producer_ids_found) == n_producers, (
            f"Expected messages from {n_producers} producers, "
            f"got from {len(producer_ids_found)}: {producer_ids_found}"
        )


class TestLoggerRotation:
    """Тесты ротации файлов."""

    def test_rotation_happens_at_max_lines(self, tmp_path):
        """Ротация происходит при достижении max_lines."""
        log_file = tmp_path / "test.log"
        max_lines = 10
        n_producers = 2
        messages_per_producer = 15  # 30 сообщений, max_lines=10 -> 2+ ротации

        logger = ThreadedLogger(
            log_path=log_file,
            max_lines=max_lines,
            n_producers=n_producers,
            messages_per_producer=messages_per_producer,
        )
        logger.start()
        logger.stop(timeout=10.0)

        # Должны быть ротированные файлы
        rotated_files = _find_rotated_files(log_file)
        assert len(rotated_files) >= 2, (
            f"Expected at least 2 rotated files for 30 messages with max_lines=10, "
            f"got {len(rotated_files)}: {rotated_files}"
        )

        # Ни один файл не должен содержать больше max_lines строк
        for f in [log_file, *rotated_files]:
            if f.exists():
                lines = f.read_text(encoding="utf-8").strip().splitlines()
                assert len(lines) <= max_lines, (
                    f"File {f.name} has {len(lines)} lines, max_lines={max_lines}"
                )

    def test_total_messages_after_rotation(self, tmp_path):
        """После ротации все сообщения сохранены (основной + ротированные файлы)."""
        log_file = tmp_path / "test.log"
        max_lines = 5
        n_producers = 2
        messages_per_producer = 10
        expected_total = n_producers * messages_per_producer

        logger = ThreadedLogger(
            log_path=log_file,
            max_lines=max_lines,
            n_producers=n_producers,
            messages_per_producer=messages_per_producer,
        )
        logger.start()
        logger.stop(timeout=10.0)

        all_lines = _collect_all_lines(log_file)
        assert len(all_lines) == expected_total, (
            f"Expected {expected_total} total messages across all files, got {len(all_lines)}"
        )


class TestLoggerShutdown:
    """Тесты корректного завершения."""

    def test_graceful_shutdown(self, tmp_path):
        """stop() корректно завершает все потоки."""
        log_file = tmp_path / "test.log"
        logger = ThreadedLogger(
            log_path=log_file,
            max_lines=1000,
            n_producers=3,
            messages_per_producer=10,
        )
        logger.start()
        logger.stop(timeout=10.0)

        # После stop() не должно быть живых потоков логгера
        # (проверяем, что stop() возвращает управление)
        # Если stop() зависнет, тест упадёт по таймауту pytest

    def test_stop_is_idempotent(self, tmp_path):
        """Повторный вызов stop() не вызывает ошибок."""
        log_file = tmp_path / "test.log"
        logger = ThreadedLogger(
            log_path=log_file,
            max_lines=1000,
            n_producers=2,
            messages_per_producer=5,
        )
        logger.start()
        logger.stop(timeout=10.0)
        logger.stop(timeout=5.0)  # Повторный вызов не должен падать

    def test_stop_within_timeout(self, tmp_path):
        """stop() завершается за разумное время."""
        log_file = tmp_path / "test.log"
        logger = ThreadedLogger(
            log_path=log_file,
            max_lines=1000,
            n_producers=3,
            messages_per_producer=50,
        )
        logger.start()

        start = time.perf_counter()
        logger.stop(timeout=10.0)
        elapsed = time.perf_counter() - start

        assert elapsed < 10.0, f"stop() took {elapsed:.2f}s, expected < 10s"


class TestLoggerMultipleProducers:
    """Тесты работы с несколькими продюсерами."""

    def test_multiple_producers_concurrent(self, tmp_path):
        """Несколько продюсеров работают параллельно без ошибок."""
        log_file = tmp_path / "test.log"
        n_producers = 5
        messages_per_producer = 20
        expected_total = n_producers * messages_per_producer

        logger = ThreadedLogger(
            log_path=log_file,
            max_lines=1000,
            n_producers=n_producers,
            messages_per_producer=messages_per_producer,
        )
        logger.start()
        logger.stop(timeout=15.0)

        all_lines = _collect_all_lines(log_file)
        assert len(all_lines) == expected_total

    def test_single_producer(self, tmp_path):
        """Работа с одним продюсером."""
        log_file = tmp_path / "test.log"
        messages_per_producer = 10

        logger = ThreadedLogger(
            log_path=log_file,
            max_lines=1000,
            n_producers=1,
            messages_per_producer=messages_per_producer,
        )
        logger.start()
        logger.stop(timeout=10.0)

        all_lines = _collect_all_lines(log_file)
        assert len(all_lines) == messages_per_producer


class TestLoggerVariant:
    """Тесты с учётом варианта студента."""

    def test_variant_primitives_are_valid(self, variant, sync_primitives):
        """Вариант определяет допустимый набор примитивов."""
        assert variant in (0, 1, 2)
        assert len(sync_primitives) == 3
        # Все примитивы — строки с названиями классов
        for prim in sync_primitives:
            assert isinstance(prim, str)
            assert prim in {"Lock", "RLock", "Semaphore", "Event", "Condition", "Barrier", "Queue"}


# ─── Вспомогательные функции ────────────────────────────────────────────────


def _find_rotated_files(log_file):
    """Найти все ротированные файлы (log_file.1, log_file.2, ...)."""
    parent = log_file.parent
    stem = log_file.name
    rotated = []
    for f in sorted(parent.iterdir()):
        if f.name.startswith(stem) and f.name != stem and f.is_file():
            rotated.append(f)
    return rotated


def _collect_all_lines(log_file):
    """Собрать все непустые строки из основного и ротированных файлов."""
    all_lines = []
    if log_file.exists():
        text = log_file.read_text(encoding="utf-8").strip()
        if text:
            all_lines.extend(text.splitlines())

    for f in _find_rotated_files(log_file):
        text = f.read_text(encoding="utf-8").strip()
        if text:
            all_lines.extend(text.splitlines())

    return all_lines
