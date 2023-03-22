import pandas

from src import quidproquo


def test_imports() -> None:
    output = quidproquo.main()
    assert isinstance(output, pandas.DataFrame)
