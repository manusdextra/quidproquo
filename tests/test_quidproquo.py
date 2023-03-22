import pandas

from src.quidproquo import main, Config


def test_imports() -> None:
    output = main()
    assert isinstance(output, pandas.DataFrame)


def test_sheet_numbers() -> None:
    config = Config()
    sourcefile = config.files[0]
    assert len(sourcefile.sheet_names) == 9
