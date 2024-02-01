from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import TypeAlias

import click

from src.library_db.database.db import Database
from src.library_db.models.book import Book

ISBN: TypeAlias = int


@dataclass
class BookStorage:
    books: dict[ISBN, Book] = field(default_factory=dict)

    def add(self, book: Book) -> None:
        self.books[book.isbn] = book

    def get_all(self) -> list[Book]:
        return sorted(self.books.values(), key=lambda book: book.year)

    def clear(self) -> None:
        self.books.clear()

    def __len__(self) -> int:
        return len(self.books)


@dataclass(frozen=True)
class Library:
    db: Database[Book]
    storage: BookStorage = field(default_factory=BookStorage)

    def initialize(self) -> None:
        for book in self.db.read():
            self.storage.add(book)
        self.save()

    def add_book(self, book: Book) -> None:
        self.storage.add(book)

    def refresh(self) -> None:
        self.storage.clear()
        books = self.db.read()
        for book in books:
            self.storage.add(book)
        self.save()

    def save(self) -> None:
        self.db.write(self.storage.get_all())

    def print_books(self) -> None:
        for book in self:
            click.secho(f"    {book!s}", fg="bright_blue")

    def count(self) -> int:
        return len(self.storage)

    def __iter__(self) -> Iterator[Book]:
        yield from self.storage.get_all()
