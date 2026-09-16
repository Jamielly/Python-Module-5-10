#!/usr/bin/env python3
from abc import ABC, abstractmethod
import typing


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._storage: list[tuple[int, str]] = []
        self._total_processed: int = 0

    @property
    def total_processed(self) -> int:
        return self._total_processed

    @property
    def pending_count(self) -> int:
        return len(self._storage)

    @abstractmethod
    def validate(self, data: typing.Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: typing.Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self._storage:
            raise IndexError("No data available to output.")
        return self._storage.pop(0)


class NumericProcessor(DataProcessor):
    def validate(self, data: typing.Any) -> bool:
        if isinstance(data, (int, float)) and not isinstance(data, bool):
            return True
        if isinstance(data, list) and data:
            return all(
                isinstance(x, (int, float)) and not isinstance(x, bool)
                for x in data
            )
        return False

    def ingest(self, data: typing.Any) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")

        items = data if isinstance(data, list) else [data]
        for item in items:
            self._storage.append((self._total_processed, str(item)))
            self._total_processed += 1


class TextProcessor(DataProcessor):
    def validate(self, data: typing.Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list) and data:
            return all(isinstance(x, str) for x in data)
        return False

    def ingest(self, data: typing.Any) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")

        items = data if isinstance(data, list) else [data]
        for item in items:
            self._storage.append((self._total_processed, item))
            self._total_processed += 1


class LogProcessor(DataProcessor):
    def validate(self, data: typing.Any) -> bool:
        def is_valid_log(d: typing.Any) -> bool:
            return (
                isinstance(d, dict)
                and all(
                    isinstance(k, str) and isinstance(v, str)
                    for k, v in d.items()
                )
            )

        if is_valid_log(data):
            return True
        if isinstance(data, list) and data:
            return all(is_valid_log(x) for x in data)
        return False

    def ingest(self, data: typing.Any) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")

        items = data if isinstance(data, list) else [data]
        for entry in items:
            level = entry.get("log_level", "INFO").strip()
            msg = entry.get("log_message", "").strip()
            formatted_log = f"{level}: {msg}"
            self._storage.append((self._total_processed, formatted_log))
            self._total_processed += 1


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[typing.Any]) -> None:
        for item in stream:
            handled = False
            for proc in self._processors:
                if proc.validate(item):
                    proc.ingest(item)
                    handled = True
                    break
            if not handled:
                print(f"Error: Unhandled stream element '{item}'")

    def print_processors_stats(self) -> None:
        print("=== Data Stream Processors Stats ===")
        for proc in self._processors:
            name = proc.__class__.__name__
            print(
                f"- {name}: {proc.total_processed} processed, "
                f"{proc.pending_count} pending in storage"
            )


def main() -> None:
    print("=== Code Nexus - Polymorphic Data Stream ===")
    stream_manager = DataStream()
    num_proc = NumericProcessor()
    text_proc = TextProcessor()
    log_proc = LogProcessor()

    stream_manager.register_processor(num_proc)
    stream_manager.register_processor(text_proc)
    stream_manager.register_processor(log_proc)
    mixed_stream: list[typing.Any] = [
        42,
        "Hello Code Nexus",
        {"log_level": "WARNING", "log_message": "Low memory"},
        [3],
        ["Python", "Polymorphism"],
        {"unsupported_type": 999},
    ]

    print("\nProcessing mixed stream...")
    stream_manager.process_stream(mixed_stream)

    print()
    stream_manager.print_processors_stats()

    print("\nConsuming items from Numeric Processor...")
    while num_proc.pending_count > 0:
        rank, val = num_proc.output()
        print(f"Extracted [{rank}]: {val}")

    print("\nConsuming items from Text Processor...")
    while text_proc.pending_count > 0:
        rank, val = text_proc.output()
        print(f"Extracted [{rank}]: {val}")

    print()
    stream_manager.print_processors_stats()


if __name__ == "__main__":
    main()
