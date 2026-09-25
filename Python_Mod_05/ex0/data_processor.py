#!/usr/bin/env python3
from abc import ABC, abstractmethod
from collections.abc import Sequence
import typing


class DataProcessor(ABC):

    def __init__(self) -> None:
        self._storage: list[tuple[int, str]] = []
        self._total_processed: int = 0

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
        if isinstance(data, bool):
            return False
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list):
            return all(
                isinstance(x, (int, float)) and not isinstance(x, bool)
                for x in data
            )
        return False

    def ingest(self, data: int | float | Sequence[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        items: Sequence[int | float]
        if isinstance(data, (int, float)):
            items = [data]
        else:
            items = data
        for item in items:
            self._storage.append((self._total_processed, str(item)))
            self._total_processed += 1


class TextProcessor(DataProcessor):

    def validate(self, data: typing.Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            return all(isinstance(x, str) for x in data)
        return False

    def ingest(self, data: str | Sequence[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")

        items: Sequence[str]
        if isinstance(data, str):
            items = [data]
        else:
            items = data
        for item in items:
            self._storage.append((self._total_processed, item))
            self._total_processed += 1


class LogProcessor(DataProcessor):

    def validate(self, data: typing.Any) -> bool:
        def is_valid_log(d: typing.Any) -> bool:
            if not isinstance(d, dict):
                return False
            return any(k in d for k in ("log_level", "log_message")) and all(
                isinstance(k, str) for k in d.keys()
            )

        if is_valid_log(data):
            return True
        if isinstance(data, list):
            return all(is_valid_log(x) for x in data)
        return False

    def ingest(
        self,
        data: dict[str, typing.Any] | Sequence[dict[str, typing.Any]],
    ) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")

        items: Sequence[dict[str, typing.Any]]
        if isinstance(data, dict):
            items = [data]
        else:
            items = data
        for entry in items:
            level = str(entry.get("log_level", "INFO")).strip()
            msg = str(entry.get("log_message", "")).strip()
            formatted_log = f"{level}: {msg}"
            self._storage.append((self._total_processed, formatted_log))
            self._total_processed += 1


def main() -> None:
    print("=== Code Nexus - Data Processor ===")

    print("\nTesting Numeric Processor...")
    num_proc = NumericProcessor()
    print(f"Trying to validate input '42': {num_proc.validate(42)}")
    print(f"Trying to validate input 'Hello': {num_proc.validate('Hello')}")
    print(f"Trying to validate empty list '[]': {num_proc.validate([])}")

    try:
        print(
            "Test invalid ingestion of string 'foo' "
            "without prior validation:"
        )
        num_proc.ingest("foo")  # type: ignore[arg-type]
    except ValueError as e:
        print(f"Got exception: {e}")

    num_data = [6, 7, 8, 9, 10]
    print(f"Processing data: {num_data}")
    num_proc.ingest(num_data)
    print("Extracting 3 values...")
    for _ in range(3):
        rank, val = num_proc.output()
        print(f"Numeric value {rank}: {val}")

    print("\nTesting Text Processor...")
    text_proc = TextProcessor()
    print(f"Trying to validate input '42': {text_proc.validate(42)}")
    text_data = ["Hello", "Nexus", "World"]
    print(f"Processing data: {text_data}")
    text_proc.ingest(text_data)
    print("Extracting 1 value...")
    rank, val = text_proc.output()
    print(f"Text value {rank}: {val}")

    print("\nTesting Log Processor...")
    log_proc = LogProcessor()
    print(f"Trying to validate input 'Hello': {log_proc.validate('Hello')}")
    log_data = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"},
    ]
    print(f"Processing data: {log_data}")
    log_proc.ingest(log_data)
    print("Extracting 2 values...")
    for _ in range(2):
        rank, val = log_proc.output()
        print(f"Log entry {rank}: {val}")


if __name__ == "__main__":
    main()
