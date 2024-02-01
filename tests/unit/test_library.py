from unittest.mock import MagicMock

from library_db.database.db import Database
from src.library_db.library import Library
from src.library_db.models.book import Book


def test_library_initialize_should_read_all_books() -> None:
    mock_db = MagicMock(spec=Database)
    mock_db.read.return_value = [
        Book(title="Test", author="Test", year=2022, isbn=int("1234567890111")),
        Book(title="Test", author="Test", year=1800, isbn=int("1234567890112")),
    ]
    library = Library(db=mock_db)
    library.initialize()
    assert library.count() == 2


def test_library_add_book_should_add_book() -> None:
    mock_db = MagicMock(spec=Database)
    mock_db.read.return_value = []
    library = Library(db=mock_db)
    library.initialize()
    library.add_book(Book(title="Test", author="Test", year=2022, isbn=int("1234567890111")))
    assert library.count() == 1


def test_library_save_should_write_all_books() -> None:
    mock_db = MagicMock(spec=Database)
    mock_db.read.return_value = []
    library = Library(db=mock_db)
    library.initialize()
    library.add_book(Book(title="Test", author="Test", year=2022, isbn=int("1234567890111")))
    library.save()
    mock_db.write.assert_called()
    assert mock_db.write.call_count == 2


def test_library_iterator_should_yield_all_books_in_ascending_order() -> None:
    mock_db = MagicMock(spec=Database)
    mock_db.read.return_value = [
        Book(title="Test", author="Test", year=2024, isbn=int("1234567890110")),
        Book(title="Test", author="Test", year=2022, isbn=int("1234567890111")),
        Book(title="Test", author="Test", year=1800, isbn=int("1234567890113")),
        Book(title="Test", author="Test", year=2001, isbn=int("1234567890114")),
    ]
    library = Library(db=mock_db)
    library.initialize()
    books = list(library)
    assert books[0].year == 1800
    assert books[1].year == 2001
    assert books[2].year == 2022
    assert books[3].year == 2024


def test_library_refresh_should_update_book_storage_correctly() -> None:
    mock_db = MagicMock(spec=Database)
    mock_db.read.return_value = [
        Book(title="Test", author="Test", year=2024, isbn=int("1234567890110")),
        Book(title="Test", author="Test", year=2022, isbn=int("1234567890111")),
        Book(title="Test", author="Test", year=1800, isbn=int("1234567890113")),
        Book(title="Test", author="Test", year=2001, isbn=int("1234567890114")),
    ]
    library = Library(db=mock_db)
    library.initialize()
    assert library.count() == 4
    mock_db.read.assert_called_once()

    mock_db.read.return_value = [
        Book(title="Test", author="Test", year=2024, isbn=int("1234567890110")),
        Book(title="Test", author="Test", year=2022, isbn=int("1234567890111")),
    ]

    library.refresh()
    assert library.count() == 2
    assert mock_db.read.call_count == 2
    assert mock_db.write.call_count == 2

    mock_db.read.return_value = []

    library.refresh()
    assert library.count() == 0
