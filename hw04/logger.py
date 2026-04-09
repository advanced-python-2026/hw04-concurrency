"""Задание 4.3 — ThreadedLogger с ротацией файлов.

Реализуйте класс ThreadedLogger:
- N потоков-продюсеров генерируют сообщения с уникальными ID
- 1 поток-консьюмер записывает в файл
- При достижении max_lines файл ротируется (создаётся новый с суффиксом .1, .2, ...)
- Корректное завершение через stop()

Вариант определяет примитивы синхронизации (см. tests/conftest.py).
"""

from __future__ import annotations

from pathlib import Path


class ThreadedLogger:
    """Многопоточный логгер с ротацией файлов.

    Args:
        log_path: путь к файлу лога
        max_lines: максимальное количество строк до ротации
        n_producers: количество потоков-продюсеров
        messages_per_producer: сколько сообщений генерирует каждый продюсер
    """

    def __init__(
        self,
        log_path: Path | str,
        max_lines: int = 100,
        n_producers: int = 3,
        messages_per_producer: int = 10,
    ) -> None:
        # TODO: инициализировать поля
        raise NotImplementedError

    def start(self) -> None:
        """Запустить продюсеров и консьюмера."""
        # TODO: реализовать
        raise NotImplementedError

    def stop(self, timeout: float = 5.0) -> None:
        """Корректно остановить все потоки.

        Args:
            timeout: максимальное время ожидания завершения каждого потока
        """
        # TODO: реализовать
        raise NotImplementedError

    def _producer(self, producer_id: int) -> None:
        """Функция потока-продюсера.

        Генерирует messages_per_producer сообщений вида:
        "[producer_id] message_number: текст сообщения"
        """
        # TODO: реализовать
        raise NotImplementedError

    def _consumer(self) -> None:
        """Функция потока-консьюмера.

        Читает сообщения из очереди/буфера и записывает в файл.
        При достижении max_lines выполняет ротацию.
        """
        # TODO: реализовать
        raise NotImplementedError

    def _rotate(self) -> None:
        """Ротация файла лога.

        Текущий файл переименовывается с суффиксом (.1, .2, ...),
        создаётся новый пустой файл.
        """
        # TODO: реализовать
        raise NotImplementedError
