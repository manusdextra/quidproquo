import pandas

from src.quidproquo import Config, filter_by_pos, import_sheets


def test_imports() -> None:
    config = Config()
    output = import_sheets(config)
    assert isinstance(output, pandas.DataFrame)


def test_concatenation() -> None:
    config = Config()
    sheets = import_sheets(config)
    assert sheets.shape == (815, 9)


def test_filter() -> None:
    config = Config()
    collection = import_sheets(config)
    assert len(filter_by_pos(collection, "n")) == 323
