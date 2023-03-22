import pandas

from src.quidproquo import Config, concat, filter_by_pos, source


def test_imports() -> None:
    config = Config()
    output = source(config.files[0])
    assert isinstance(output[0], pandas.DataFrame)


def test_sheet_numbers() -> None:
    config = Config()
    sheets = source(config.files[0])
    assert len(sheets) == 9


def test_concatenation() -> None:
    config = Config()
    sheets = source(config.files[0])
    df = concat(sheets)
    assert df.shape == (815, 9)


def test_filter() -> None:
    config = Config()
    collection = concat(source(config.files[0]))
    assert filter_by_pos(collection, "n").shape == (323, 3)
