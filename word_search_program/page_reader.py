"""This reads a page using PDFPlumber"""

from typing import Union
import pdfplumber
import re

UNITS_MAP = {
    "millions": 1000000,
    "million": 1000000,
    "billions": 1000000000,
    "billion": 1000000000,
    "thousands": 1000,
    "thousand": 1000,
}
"""Maps unit definitions to multiplication factors."""

END_WORD_PUNC = [".", ":", ";", "!", "$", ")", '"', "'", "}", "?", "]"]


def _is_number(word: str) -> Union[bool, float]:
    """Returns True if the word is numeric and false otherwise."""
    period_count = 0
    if word[-1] in END_WORD_PUNC:
        word = word[: len(word) - 1]

    word = word.replace("$", "")

    for letter in word:
        if letter not in ".,0123456789":
            return False
        if letter == ".":
            period_count += 1

    number = word.replace(",", "")

    if len(number) == 0:
        return False

    if period_count > 1:
        return False

    return float(number)


def _adjust_units(number: float, units: str = None) -> float:
    """Returns the number and adjusted for units if it can be."""
    if units[-1] in END_WORD_PUNC:
        units = units[: len(units) - 1]

    if units.lower() in UNITS_MAP:
        return number * UNITS_MAP[units.lower()]
    else:
        return number


def process_page(page: pdfplumber.PDF):
    """Returns the largest number from a pdf page without processing tables."""
    largest_number = 0
    word_list = page.extract_text().replace("\n", " ").split(" ")

    for i in range(len(word_list)):
        word = word_list[i]
        if i + 1 < len(word_list) - 1:
            number = _adjust_units(_is_number(word), word_list[i + 1])
        else:
            number = _is_number(word)
        if number and number > largest_number:
            largest_number = number

    # Try processing tables now.
    tables = page.extract_tables()
    for table in tables:
        largest_in_table = process_table(table)
        if largest_in_table > largest_number:
            largest_number = largest_in_table
    return largest_number


def process_table(table) -> float:
    """Processes a table, assumes that any units listed in the table will be the same."""
    largest_number = 0
    units = None
    for cell in table:
        if units:
            break
        if isinstance(cell, str) and cell.lower() in UNITS_MAP:
            units = cell.lower()
        for string in cell:
            if string is None:
                continue
            words = re.sub(r"[^\w\s]", "", string).split(" ")
            for word in words:
                if units:
                    break
                if word.lower() in UNITS_MAP:
                    units = word.lower()

    for cell in table:
        if isinstance(cell, str):
            number = _is_number(cell)
            if number and units:
                if largest_number < _adjust_units(number, units):
                    largest_number = _adjust_units(number, units)
            elif number:
                if largest_number < number:
                    largest_number = number
        else:
            for word in cell:
                if word:
                    number = _is_number(word)
                    if number and units:
                        if largest_number < _adjust_units(number, units):
                            largest_number = _adjust_units(number, units)
                    elif number:
                        if largest_number < number:
                            largest_number = number
    return largest_number
