"""
Quid Pro Quo

Take an Excel spreadsheet full of vocabulary and turn it into a Kahoot Quiz
"""

import pathlib

import pandas


Word = tuple[str, str, str]


class Config:
    """
    Collection of important variables such as source file locations
    """

    # this is necessary because the REPL doesn't have access to __file__
    try:
        root = pathlib.Path(__file__).parents[1]
    except NameError:
        root = pathlib.Path("/home/henning/code/projects/quidproquo")
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
) -> list[Word]:
    """
    Return a new DataFrame containing only the specified parts of speech.
    If a word has several meanings, this will split them into separate definitions,
    one for each part of speech.
    """
    all_words = dframe[(dframe["Part of speech"] == pos)][["Word", "Definition"]]
    words = []
    separator = ", "
    if separator not in pos:
        for word, definition in all_words.itertuples(index=False):
            words.append((word, pos, definition))
        return words
    pos1, pos2 = pos.split(separator)
    for word, definitions in all_words.itertuples(index=False):
        if "\n" in definitions:
            def1, def2 = definitions.split("\n")
            # cut leading numbers
            def1 = def1[3:]
            def2 = def2[3:]
        else:
            def1 = definitions
            def2 = definitions
        words.append((word, pos1, def1))
        words.append((word, pos2, def2))
    return words


def sort_by_pos(collection: list[Word]):
    sorted_words = {}
    for item in collection:
        word, pos, definition = item
        try:
            sorted_words[pos].append((word, definition))
        except KeyError:
            sorted_words[pos] = [(word, definition)]
    return sorted_words


def main():
    conf = Config()
    collection = source_files(conf)

    pos_list = list_pos(collection)
    unsorted_words = []
    for pos in pos_list:
        unsorted_words.extend(filter_by_pos(collection, pos))
    sorted_words = sort_by_pos(unsorted_words)
    return sorted_words


if __name__ == "__main__":
    complete = main()
