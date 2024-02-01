from datetime import date

import pytest

from src.library_db.models.book import Book


def test_book_should_have_author_title_year_isbn() -> None:
    book = Book(author="author", title="title", year=2000, isbn=1234567891234)
    assert book.author == "author"
    assert book.title == "title"
    assert book.year == 2000
    assert book.isbn == 1234567891234


def test_book_should_have_str_representation() -> None:
    book = Book(author="author", title="title", year=2000, isbn=1234567891234)
    assert str(book) == "title by author (2000, ISBN: 1234567891234)"


def test_book_should_have_repr_representation() -> None:
    book = Book(author="author", title="title", year=2000, isbn=1234567891234)
    assert repr(book) == "Book(title=title, author=author, year=2000, isbn=1234567891234)"


def test_book_should_be_frozen() -> None:
    book = Book(author="author", title="title", year=2000, isbn=1234567891234)
    with pytest.raises(AttributeError):
        book.author = "new author"  # type: ignore
    with pytest.raises(AttributeError):
        book.title = "new title"  # type: ignore
    with pytest.raises(AttributeError):
        book.year = 2001  # type: ignore
    with pytest.raises(AttributeError):
        book.isbn = 1234567891235  # type: ignore


def test_book_to_row_should_return_list_of_strings() -> None:
    book = Book(author="author", title="title", year=2000, isbn=1234567891234)
    assert book.to_row() == ["title", "author", "1234567891234", "2000"]


def test_book_from_row_should_return_book() -> None:
    book = Book.from_row(["title", "author", "1234567891234", "2000"])
    assert book == Book(author="author", title="title", year=2000, isbn=1234567891234)


def test_book_post_init_should_raise_value_error_if_title_is_empty() -> None:
    with pytest.raises(ValueError):
        Book(author="author", title="", year=2000, isbn=1234567891234)


def test_book_post_init_should_raise_value_error_if_author_is_empty() -> None:
    with pytest.raises(ValueError):
        Book(author="", title="title", year=2000, isbn=1234567891234)


@pytest.mark.parametrize(
    "year",
    [
        pytest.param(-1, id="negative"),
        pytest.param(date.today().year + 1, id="too large"),
    ],
)
def test_book_post_init_should_raise_value_error_if_year_is_invalid(year: int) -> None:
    with pytest.raises(ValueError):
        Book(author="author", title="title", year=year, isbn=1234567891234)


@pytest.mark.parametrize(
    "isbn",
    [
        pytest.param(-1, id="negative"),
        pytest.param(123456789, id="too short"),
        pytest.param(12345678912345, id="too long"),
    ],
)
def test_book_post_init_should_raise_value_error_if_isbn_is_invalid(isbn: int) -> None:
    with pytest.raises(ValueError):
        Book(author="author", title="title", year=2000, isbn=isbn)
