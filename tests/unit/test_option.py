from src.library_db.option import Option


def test_option_creation() -> None:
    assert all([Option.ADD.value == 1, Option.PRINT.value == 2, Option.QUIT.value == "Q"])
