import csv
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, TypeVar, runtime_checkable

from src.library_db.models.book import Book

TDatabaseModel = TypeVar("TDatabaseModel")


@runtime_checkable
class Database(
    Protocol[TDatabaseModel],
):
    def read(self, delimiter: str = "/") -> Sequence[TDatabaseModel]: ...

    def write(self, items: Sequence[TDatabaseModel]) -> None: ...


@runtime_checkable
class SupportsToRow(
    Protocol,
):
    def to_row(self) -> list[str]: ...


@dataclass(frozen=True)
class FileDatabase:
    file_path: Path
    delimiter: str = "/"

    def read(self, delimiter: str = "/") -> list[Book]:
        with Path(self.file_path).open() as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=delimiter)
            return [Book.from_row(row) for row in csv_reader if row]

    def write(self, items: Sequence[SupportsToRow]) -> None:
        with Path(self.file_path).open("w") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=self.delimiter)
            for item in items:
                csv_writer.writerow(item.to_row())
