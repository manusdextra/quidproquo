import pandas
import pathlib


def main():
    sourcefile = pandas.ExcelFile(
        pathlib.Path(__file__).parents[1]
        / "inputs"
        / "Gold_Exp_B1P_ExpandedWordlist.xlsx"
    )
    dataframe = pandas.read_excel(sourcefile)
    return dataframe
