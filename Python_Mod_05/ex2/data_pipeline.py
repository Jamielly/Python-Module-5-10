#!/usr/bin/env python3
from abc import ABC, abstractmethod
import json
from typing import Any, Protocol


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
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self._storage:
            raise IndexError("No data available to output.")
        return self._storage.pop(0)


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)) and not isinstance(data, bool):
            return True
        if isinstance(data, list) and data:
            return all(
                isinstance(x, (int, float)) and not isinstance(x, bool)
                for x in data
            )
        return False

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")

        items = data if isinstance(data, list) else [data]
        for item in items:
            self._storage.append((self._total_processed, str(item)))
            self._total_processed += 1


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list) and data:
            return all(isinstance(x, str) for x in data)
        return False

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")

        items = data if isinstance(data, list) else [data]
        for item in items:
            self._storage.append((self._total_processed, item))
            self._total_processed += 1


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        def is_valid_log(d: Any) -> bool:
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

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")

        items = data if isinstance(data, list) else [data]
        for entry in items:
            level = entry.get("log_level", "INFO").strip()
            msg = entry.get("log_message", "").strip()
            formatted_log = f"{level}: {msg}"
            self._storage.append((self._total_processed, formatted_log))
            self._total_processed += 1


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class CSVPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        if not data:
            return

        values = [val for _, val in data]
        csv_string = ",".join(values)
        print(f"CSV Output: {csv_string}")


class JSONPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        if not data:
            return
        json_dict = {f"item_{rank}": val for rank, val in data}
        json_string = json.dumps(json_dict)
        print(f"JSON Output: {json_string}")


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
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
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
            return
        for proc in self._processors:
            name = proc.__class__.__name__
            formatted_name = name.replace("Processor", " Processor")
            print(
                f"{formatted_name}: total {proc.total_processed} items "
                f"processed, remaining {proc.pending_count} on processor"
            )

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self._processors:
            extracted: list[tuple[int, str]] = []
            for _ in range(nb):
                if proc.pending_count == 0:
                    break
                extracted.append(proc.output())
            if extracted:
                plugin.process_output(extracted)


def main() -> None:
    print("=== Code Nexus - Data Pipeline ===")

    print("Initialize Data Stream...")
    stream = DataStream()
    stream.print_processors_stats()

    print("\nRegistering Processors")
    num_proc = NumericProcessor()
    text_proc = TextProcessor()
    log_proc = LogProcessor()

    stream.register_processor(num_proc)
    stream.register_processor(text_proc)
    stream.register_processor(log_proc)

    batch1: list[Any] = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {"log_level": "WARNING", "log_message": "Telnet access! Use ssh"},
            {"log_level": "INFO", "log_message": "User wil is connected"},
        ],
        42,
        ["Hi", "five"],
    ]

    print("\nSend first batch of data on stream:", batch1)
    stream.process_stream(batch1)
    stream.print_processors_stats()

    csv_plugin = CSVPlugin()
    print("\nSend 3 processed data from each processor to a CSV plugin:")
    stream.output_pipeline(3, csv_plugin)
    stream.print_processors_stats()

    batch2: list[Any] = [
        21,
        ["I am fine", "James", "Stay here"],
        [
            {"log_level": "ERROR", "log_message": "500 server crash"},
            {
                "log_level": "NOTICE",
                "log_message": "Certificate expires in 10 days",
            },
        ],
        [4 - 7],
        "World hello",
    ]

    print("\nSend another batch of data:", batch2)
    stream.process_stream(batch2)
    stream.print_processors_stats()

    json_plugin = JSONPlugin()
    print("\nSend 5 processed data from each processor to a JSON plugin:")
    stream.output_pipeline(5, json_plugin)
    stream.print_processors_stats()


if __name__ == "__main__":
    main()
