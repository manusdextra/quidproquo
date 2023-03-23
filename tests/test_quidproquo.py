import pandas

from src.quidproquo import Config, filter_by_pos, source_files


def test_imports() -> None:
    config = Config()
    output = source_files(config)
    assert isinstance(output, pandas.DataFrame)


def test_concatenation() -> None:
    config = Config()
    sheets = source_files(config)
    assert sheets.shape == (815, 9)


def test_filter() -> None:
    config = Config()
    collection = source_files(config)
    assert len(filter_by_pos(collection, "n")) == 323
