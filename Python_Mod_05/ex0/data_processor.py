#!/usr/bin/env python3

from abc import ABC, abstractmethod
import typing

class DataProcessor(ABC):

    def __init__(self) -&gt; None:
        self._storage: list[tuple[int, str]] = []
        self._total_processed: int = 0

    @abstractmethod
    def validate(self, data: typing.Any) -&gt; bool:
        pass

    @abstractmethod
    def ingest(self, data: typing.Any) -&gt; None:
        pass

    def output(self) -&gt; tuple[int, str]:
        if not self._storage:
            raise IndexError("No data available to output.")
        return self._storage.pop(0)

class NumericProcessor(DataProcessor):

    def validate(self, data: typing.Any) -&gt; bool:
        if isinstance(data, (int, float)) and not isinstance(data, bool):
            return True
        if isinstance(data, list) and data:
            return all(
                isinstance(x, (int, float)) and not isinstance(x, bool)
                for x in data
            )
        return False

    def ingest(self, data: int | float | list[int | float]) -&gt; None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")

        items = data if isinstance(data, list) else [data]
        for item in items:
            self._storage.append((self._total_processed, str(item)))
            self._total_processed += 1

class TextProcessor(DataProcessor):

    def validate(self, data: typing.Any) -&gt; bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list) and data:
            return all(isinstance(x, str) for x in data)
        return False

    def ingest(self, data: str | list[str]) -&gt; None:
        if not self.validate(data):
            raise ValueError("Improper text data")

        items = data if isinstance(data, list) else [data]
        for item in items:
            self._storage.append((self._total_processed, item))
            self._total_processed += 1

class LogProcessor(DataProcessor):

    def validate(self, data: typing.Any) -&gt; bool:
        def is_valid_log(d: typing.Any) -&gt; bool:
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

    def ingest(
        self, data: dict[str, str] | list[dict[str, str]]
    ) -&gt; None:
        if not self.validate(data):
            raise ValueError("Improper log data")

        items = data if isinstance(data, list) else [data]
        for entry in items:
            level = entry.get("log_level", "INFO").strip()
            msg = entry.get("log_message", "").strip()
            formatted_log = f"{level}: {msg}"
            self._storage.append((self._total_processed, formatted_log))
            self._total_processed += 1

def main() -&gt; None:
    print("=== Code Nexus - Data Processor ===")

    print("\nTesting Numeric Processor...")
    num_proc = NumericProcessor()
    print(f"Trying to validate input '42': {num_proc.validate(42)}")
    print(f"Trying to validate input 'Hello': {num_proc.validate('Hello')}")

    try:
        print("Test invalid ingestion of string 'foo' without prior validation:")
        num_proc.ingest("foo")  # type: ignore[arg-type]
    except ValueError as e:
        print(f"Got exception: {e}")

    num_data = [6-10]
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