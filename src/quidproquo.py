"""
Quid Pro Quo

Take an Excel spreadsheet full of vocabulary and turn it into a Kahoot Quiz
"""

import pathlib

import pandas


class Config:
    """
    Collection of important variables such as source file locations
    """

    root = pathlib.Path(__file__).parents[1]
    inputs = root / "inputs"
    output = root / "output"

    @property
    def files(self) -> list:
        """load all input files into memory"""
        return [pandas.ExcelFile(file) for file in self.inputs.iterdir()]

    @property
    def template(self) -> pandas.DataFrame:
        """provide kahoot template and select appropriate regions"""
        return pandas.read_excel(
            self.root / "template.xlsx",
            engine="openpyxl",
            skiprows=7,
            index_col=0,
        )


def source_files(config: Config) -> pandas.DataFrame:
    """
    Load files and analyse them
    """
    sourcefile = config.files[0]
    sheets = [
        pandas.read_excel(sourcefile, sheet_name=sheet_name, engine="openpyxl")
        for sheet_name in sourcefile.sheet_names
    ]
    return pandas.concat(sheets)


def list_pos(
    dframe: pandas.DataFrame,
) -> list[str]:
    """
    Make a list of parts of speech included in the set, sorted by Frequency,
    optionally with duplicates ("noun, verb" and "verb, noun" for example) removed.
    """
    return list(dframe["Part of speech"].value_counts().index)


def filter_by_pos(
    dframe: pandas.DataFrame,
    pos: str,
) -> list[tuple[str, str, str]]:
    """
    Return a new DataFrame containing only the specified parts of speech.
    If a word has several meanings, this will split them into separate definitions,
    one for each part of speech.
    """
    whole = dframe[(dframe["Part of speech"] == pos)][["Word", "Definition"]]
    separator = ", "
    if separator not in pos:
        return whole
    pos1, pos2 = pos.split(separator)
    tuples = []
    for tup in whole.itertuples(index=False):
        if "\n" in tup[1]:
            def1, def2 = tup[1].split("\n")
            # cut leading numbers
            def1 = def1[3:]
            def2 = def2[3:]
        else:
            def1 = tup[1]
            def2 = tup[1]
        tuples.append(
            (tup[0], pos1, def1),
        )
        tuples.append(
            (tup[0], pos2, def2),
        )
    return tuples


if __name__ == "__main__":
    conf = Config()
    collection = source_files(conf)

    parts_of_speech = list_pos(collection)
