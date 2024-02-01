ISBN_LENGTH = 13


def validate_isbn(isbn: int) -> None:
    if isbn < 0 or len(str(isbn)) != ISBN_LENGTH:
        raise ValueError(f"ISBN must be a positive integer with {ISBN_LENGTH} digits! Got: {isbn}")
