from datetime import date


def validate_year(year: int) -> None:
    if not (0 <= year <= date.today().year):
        raise ValueError(
            f"Year must be a positive integer between 0 and {date.today().year}! Got: {year}"
        )
