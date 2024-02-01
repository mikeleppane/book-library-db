from datetime import date

import pytest

from src.library_db.utils.isbn import validate_isbn
from src.library_db.utils.year import validate_year


@pytest.mark.parametrize(
    "year",
    [
        pytest.param(-1, id="negative"),
        pytest.param(date.today().year + 1, id="too large"),
    ],
)
def test_validate_year_should_raise_value_error(year: int) -> None:
    with pytest.raises(ValueError):
        validate_year(year)


@pytest.mark.parametrize(
    "year",
    [
        pytest.param(0, id="lower bound"),
        pytest.param(1, id="positive"),
        pytest.param(date.today().year, id="upper bound"),
    ],
)
def test_validate_year_should_not_raise_value_error(year: int) -> None:
    validate_year(year)


@pytest.mark.parametrize(
    "isbn",
    [
        pytest.param(-1, id="negative"),
        pytest.param(123456789, id="too short"),
        pytest.param(12345678912345, id="too long"),
    ],
)
def test_validate_isbn_should_raise_value_error(isbn: int) -> None:
    with pytest.raises(ValueError):
        validate_isbn(isbn)


@pytest.mark.parametrize(
    "isbn",
    [
        pytest.param(1234567891234, id="positive"),
        pytest.param(9999999999999, id="upper bound"),
    ],
)
def test_validate_isbn_should_not_raise_value_error(isbn: int) -> None:
    validate_isbn(isbn)
