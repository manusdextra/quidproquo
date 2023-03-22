import pandas

from src.quidproquo import source, Config


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
    df = pandas.concat(sheets)
    assert df.shape == (815, 9)
