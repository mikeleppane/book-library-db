from datetime import date
from enum import Enum
from typing import Self

import click

from src.library_db.utils.isbn import validate_isbn
from src.library_db.utils.year import validate_year


class Option(Enum):
    ADD = 1
    PRINT = 2
    QUIT = "Q"

    @classmethod
    def choose(cls) -> Self:
        while True:
            try:
                command = input("Choose option: ")
                if command == "Q":
                    return cls(command)
                return cls(int(command))
            except ValueError:
                click.echo("Invalid option!")
                click.echo("Please enter a valid option (1 (add), 2 (print) or Q (quit)).")
                continue

    @classmethod
    def ask_author(cls) -> str:
        while True:
            author = input("  Author: ")
            if author:
                return author
            click.echo("  Author must not be empty!")

    @classmethod
    def ask_title(cls) -> str:
        while True:
            title = input("  Title: ")
            if title:
                return title
            click.echo("  Title must not be empty!")

    @classmethod
    def ask_year(cls) -> int:
        while True:
            try:
                year = int(input("  Year: "))
                validate_year(year)
                return year
            except ValueError as ex:
                click.echo("  Invalid year!")
                click.echo(f"  Error: {ex}")
                click.echo(f"  Please enter a valid year (0 <= year <= {date.today().year})")
                continue

    @classmethod
    def ask_isbn(cls) -> int:
        while True:
            try:
                isbn = int(input("  ISBN: "))
                validate_isbn(isbn)
                return isbn
            except ValueError as ex:
                click.echo("  Invalid ISBN!")
                click.echo(f"  Error: {ex}")
                click.echo("  Please enter a valid ISBN (13 digits)")
                continue

    @classmethod
    def ask_to_update(cls) -> bool:
        while True:
            answer = input("  Do you want to update this book? (y/n) ")
            if answer.lower() == "y":
                return True
            if answer.lower() == "n":
                return False
            click.echo("  Invalid answer!")
            click.echo("  Please enter 'y' or 'n'.")

    @classmethod
    def print_options(cls) -> None:
        click.echo()
        click.echo("Options:")
        click.echo("  1. Add book")
        click.echo("  2. Print books")
        click.echo("  Q. Quit")
