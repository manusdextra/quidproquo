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

    inputs = pathlib.Path(__file__).parents[1] / "inputs"

    @property
    def files(self) -> list:
        return [pandas.ExcelFile(file) for file in self.inputs.iterdir()]


def main():
    """
    Load files and analyse them
    """
    config = Config()

    sourcefile = config.files[0]
    dataframe = pandas.read_excel(sourcefile)
    return dataframe
