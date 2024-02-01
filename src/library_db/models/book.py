from dataclasses import dataclass
from typing import Self

from src.library_db.utils.isbn import validate_isbn
from src.library_db.utils.year import validate_year


@dataclass(frozen=True)
class Book:
    title: str
    author: str
    year: int
    isbn: int

    @classmethod
    def from_row(cls, row: list[str]) -> Self:
        try:
            title, author, isbn, year = row
        except ValueError as ex:
            raise ValueError(f"Invalid row: {row}") from ex
        return cls(title=title, author=author, year=int(year), isbn=int(isbn))

    def to_row(self) -> list[str]:
        return [self.title, self.author, str(self.isbn), str(self.year)]

    def __post_init__(self) -> None:
        validate_year(self.year)
        validate_isbn(self.isbn)
        if not self.title:
            raise ValueError("Title must not be empty!")
        if not self.author:
            raise ValueError("Author must not be empty!")

    def __str__(self) -> str:
        return f"{self.title} by {self.author} ({self.year}, ISBN: {self.isbn})"

    def __repr__(self) -> str:
        return f"Book(title={self.title}, author={self.author}, year={self.year}, isbn={self.isbn})"
