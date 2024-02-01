import sys
from dataclasses import dataclass
from pathlib import Path

import click

from src.library_db import __version__
from src.library_db.database.db import FileDatabase
from src.library_db.library import Library
from src.library_db.models.book import Book
from src.library_db.option import Option


@dataclass(frozen=True)
class CLI:
    database_file: Path
    library: Library

    def init(self) -> None:
        click.secho("Welcome to the library database CLI!", fg="green")
        click.echo(f"Reading database file: {self.database_file}")
        try:
            self.library.initialize()
        except (OSError, ValueError) as ex:
            click.secho(
                f"😔 An error occurred while reading database file ({self.database_file})", fg="red"
            )
            click.echo(f"Error: {ex}")
            click.echo("Please check the file and try again.")
            click.echo("Exiting...")
            sys.exit(1)
        click.echo(f"Database file ({self.database_file}) OK. Found {self.library.count()} books.")
        click.echo("=====================================")
        click.echo("What would you like to do?")

    def run(self) -> None:
        while True:
            Option.print_options()
            match Option.choose():
                case Option.ADD:
                    self.handle_add()
                case Option.PRINT:
                    self.handle_print()
                case Option.QUIT:
                    self.handle_quit()
                    break

    def handle_add(self) -> None:
        click.echo("Enter book details:")
        author = Option.ask_author()
        title = Option.ask_title()
        year = Option.ask_year()
        isbn = Option.ask_isbn()
        book = Book(title=title, author=author, year=year, isbn=isbn)
        click.echo(f"\n  Entered book: {book!s}")
        should_update = Option.ask_to_update()
        if not should_update:
            return
        self.library.add_book(Book(title=title, author=author, year=year, isbn=isbn))
        try:
            self.library.save()
        except OSError as ex:
            click.secho("😔 An error occurred while saving database file!", fg="red")
            click.echo(f"Error: {ex}")
            click.echo("Please check the file and try again.")
            click.echo("Exiting...")
            sys.exit(1)

    def handle_print(self) -> None:
        try:
            self.library.refresh()
        except (OSError, ValueError) as ex:
            click.secho(
                f"😔 An error occurred while reading database file ({self.database_file})", fg="red"
            )
            click.echo(f"Error: {ex}")
            click.echo("Please check the file and try again.")
            click.echo("Exiting...")
            sys.exit(1)
        if self.library.count() == 0:
            click.echo("===== **** =====")
            click.secho("📃 Database is empty!", fg="yellow")
            click.echo("===== **** =====")
            return
        click.echo("===== **** =====")
        click.secho("📃 Database content:", fg="green")
        self.library.print_books()
        click.echo("===== **** =====")

    def handle_quit(self) -> None:
        click.echo("👋 Bye!")


@click.command(
    help="This is a simple simulator for generating ROA messages and sending those to AMQP."
)
@click.version_option(__version__, prog_name="Library book database CLI")
@click.argument(
    "database_file",
    required=True,
    type=click.Path(
        exists=True,
        file_okay=True,
        readable=True,
        path_type=Path,
    ),
)
def cli(database_file: Path) -> None:
    cli = CLI(database_file=database_file, library=Library(db=FileDatabase(database_file)))
    cli.init()
    cli.run()
