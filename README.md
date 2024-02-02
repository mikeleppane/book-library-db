[![Library DB - Continuous Integration](https://github.com/mikeleppane/book-library-db/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/mikeleppane/book-library-db/actions/workflows/ci.yml)

# Library DB

## Description

Library DB is a simple database application (CLI) for managing a book library. The application is built with Python. The application uses a file as a database which the user will give as an argument when starting the application.

## Features

- Add books to the library
- Print all books in the library
- Possibility to edit book information in the database at runtime

## Installation

### Prerequisites

- Python 3.11 or newer
- [Poetry](https://python-poetry.org/)
- [pyenv](https://github.com/pyenv/pyenv) (optional, recommended) for managing Python versions

### Steps

1. Clone the repository
2. Setup Python version with `pyenv install 3.11.6 (or 3.12.0)` and take it into use with `pyenv local 3.11.6 (or 3.12.0)`. If you don't want to use `pyenv`, you can skip this step or you already have the correct Python version installed.
3. Tell Poetry which Python version to use with `poetry env use <python_version>`. For example, if you want to use Python 3.11.6, you can use `poetry env use 3.11.6`.
4. Install dependencies with `poetry install` or `poetry install --only main` if you don't want to install development dependencies.

## Project Structure

```bash
├── .github/workflows  # CI configuration
│   └── ci.yml
├── .gitignore 
├── Makefile  # Makefile for running common commands
├── poetry.lock 
├── pyproject.toml  # Poetry configuration
├── app.py # Main application
├── README.md
├── src  # Source code
│   ├── library_db
│   │   ├── __init__.py
│   │   ├── database  # Database related code
│   │   ├── models  # Domain models
│   │   ├── utils  # Utility functions
│   │   └── cli.py  # Command line interface
│   │   └── library.py  # Library class to represent the library
│   │   └── option.py  # Option class to represent command line options
├── tests  # Tests
│   ├── unit  # Unit tests
```

## Usage

### Starting the application

The application can be started with `poetry run python app.py <database_file>` in the project root (you can also spawn a shell run command from there => `poetry shell`, `python app.py <database_file>`).
For example, if you want to use `library.db` as the database file, you can start the application with `poetry run python -m library_db library.db`.

### Command line options

The application supports the following command line options:

- `--help` or `-h`: Prints help message
- `--version` or `-v`: Prints application version

### Database file

The application uses a file as a database. Each row in the file represents a book and only one book per row is allowed.
The database file must be in the following format:

```text
title/author/isbn/year (Book 1) 
title/author/isbn/year (Book 2)
```

The file can contain any number of books. The application assumes that the file is in the correct format and contains valid data. If the file is not in the correct format or otherwise contains invalid data, the application will print an error message and exit. In addition, the file can contain empty lines. Those lines will be ignored and removed when the application sync the database file.

### How to use the application

When the application is started, you will see the following menu:

```bash
Welcome to the library database CLI!
Reading database file: library.db
Database file (library.db) OK. Found 2 books.
=====================================
What would you like to do?

Options:
  1. Add book
  2. Print books
  Q. Quit
Choose option:
```

`Note:` The application assumes that the database file exists and is in the correct format. If the file does not exist, the application will exit. If the file is not in the correct format or otherwise contains invalid data, the application will print an error message and exit.

You can choose an option by typing an option and pressing enter. The following options are available:

- `1`: Add book
- `2`: Print books
- `Q`: Quit

#### Adding a book

When you choose option `1`, you will be asked to enter the book information. The following information is required:

- Title (cannot be empty)
- Author (cannot be empty)
- Year (must be a valid year, 0 <= year <= current year)
- ISBN (must be a valid ISBN, positive integer with 13 digits)

The application will ask you to enter the information until you enter valid information. The application will print an error message if you enter invalid information.

After you have entered valid information, the application will ask for confirmation: 

```bash
Entered book: Book by Author (Year, ISBN: *************)
Do you want to update this book? (y/n) y
```

If you confirm, the book will be added to the database. Otherwise, the application will ignore the book and return to the main menu.

#### Printing books

When you choose option `2`, the application will print all books in the database in ascending order. The books will be printed in the following format:

```bash
===== **** =====
📃 Database content:
    Book by Author (Year, ISBN: *************)
===== **** =====

```

#### Quitting the application

When you choose option `Q`, the application will exit.

`Note:` If a user edits the database file at runtime, the application will not directly notice the changes. However, if the user chooses either option `1` or `2`, the application will read the database file again and will reflect the changes.

## Development

### Setting up the development environment

1. Clone the repository
2. Install dependencies with `poetry install`

### Testing

The application uses [pytest](https://docs.pytest.org/en/latest/) for testing. You can run the tests with `make test` or use `pytest` directly.

### Code Quality

The application uses `mypy`, `ruff`, `isort` and `black` for managing code quality. You can run all checks with `make check` or use the tools directly.

Tools configuration is located in `pyproject.toml`.

## LICENSE

[MIT License](https://opensource.org/license/mit/)
