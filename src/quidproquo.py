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
    template = root / "template.xlsx"
    inputs = root / "inputs"
    output = root / "output"

    @property
    def files(self) -> list:
        return [pandas.ExcelFile(file) for file in self.inputs.iterdir()]


def source(sourcefile: pandas.ExcelFile) -> list[pandas.DataFrame]:
    """
    Load files and analyse them
    """

    return [
        pandas.read_excel(sourcefile, sheet_name=sheet_name, engine="openpyxl")
        for sheet_name in sourcefile.sheet_names
    ]


if __name__ == "__main__":
    config = Config()

    sheets = source(config.files[0])
    complete_collection = pandas.concat(sheets)
