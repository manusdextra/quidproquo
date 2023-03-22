"""
Quid Pro Quo

Take an Excel spreadsheet full of vocabulary and turn it into a Kahoot Quiz
"""

import pandas
import pathlib


class Config:
    """
    Collection of important variables such as source file locations
    """

    root = pathlib.Path(__file__).parents[1]
    inputs = root / "inputs"
    output = root / "output"

    @property
    def files(self) -> list:
        return [pandas.ExcelFile(file) for file in self.inputs.iterdir()]

    @property
    def template(self) -> pandas.DataFrame:
        return pandas.read_excel(
            self.root / "template.xlsx",
            engine="openpyxl",
            skiprows=7,
            index_col=0,
        )


def source(sourcefile: pandas.ExcelFile) -> list[pandas.DataFrame]:
    """
    Load files and analyse them
    """

    return [
        pandas.read_excel(sourcefile, sheet_name=sheet_name, engine="openpyxl")
        for sheet_name in sourcefile.sheet_names
    ]


def list_pos(
    df: pandas.DataFrame,
) -> list[str]:
    """
    Make a list of parts of speech included in the set, sorted by Frequency,
    optionally with duplicates ("noun, verb" and "verb, noun" for example) removed.
    """
    return list(df["Part of speech"].value_counts().index)


def filter_by_pos(
    df: pandas.DataFrame,
    pos: str,
) -> pandas.DataFrame:
    """
    Return a new DataFrame containing only the specified parts of speech
    """
    return df[(df["Part of speech"] == pos)][["Word", "Definition"]]


def concat(sheets: list[pandas.DataFrame]) -> pandas.DataFrame:
    return pandas.concat(sheets)


if __name__ == "__main__":
    config = Config()
    complete_collection = concat(source(config.files[0]))

    parts_of_speech = list_pos(complete_collection)
