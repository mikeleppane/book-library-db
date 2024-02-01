from pathlib import Path

from library_db.models.book import Book
from src.library_db.database.db import FileDatabase


def test_file_database_should_read_and_write() -> None:
    books = [
        Book(title="Test", author="Test", year=2000 + i, isbn=int(f"123456789011{i}"))
        for i in range(10)
    ]

    database = FileDatabase(file_path=Path("./tests/unit/test_data_db.txt"))

    database.write(books)

    assert str(database.read()) == str(books)
