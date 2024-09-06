"""This module contains simple unit tests for the program."""

from word_search_program.page_reader import _is_number, process_page, _adjust_units
import pytest
from typing import Union


@pytest.mark.parametrize(
    "word,number_bool",
    [
        ("notNumber", False),
        ("10", 10),
        ("10.1", 10.1),
        ("1,000", 1000),
        ("1000.", 1000),
        ("1.1.1.1.1", False),
    ],
)
def test_is_number(word: str, number_bool: bool):
    number = _is_number(word)
    if number:
        assert number == number_bool
    else:
        assert number == number_bool


class _mock_pdfplumber:
    """This class stores a mock the pdfplumber PDF class, since PDF's are hard to create in a module."""

    def __init__(self, page: str):
        self.page = page

    def extract_text(self):
        """Returns the page in order to mock the PDF plumber functionality."""
        return self.page
            
    def extract_tables(self):
        """Does not accurately mock table extraction."""
        return []


@pytest.mark.parametrize(
    "page, largest_number",
    [
        (_mock_pdfplumber("1000, no other numbers"), 1000),
        (_mock_pdfplumber("Lots of numbers: 1, 2, 3, and 4"), 4),
        (_mock_pdfplumber("4, 3, 2, 1, lots of numbers"), 4),
    ],
)
def test_process_page(page, largest_number: Union[int, float]):
    """Tests that the pdf processor returns the largest number from a page."""
    print(page.extract_text())
    assert largest_number == process_page(page)


@pytest.mark.parametrize(
    "number,units,expected_number",
    [
        (10, "million", 10000000),
        (10, "millions", 10000000),
        (10, "billion", 10000000000),
        (10, "billions", 10000000000),
        (10, "thousand", 10000),
        (10, "thousands", 10000),
        (10, "noUnits", 10),
    ],
)
def test_adjust_units(number: float, units: str, expected_number: float):
    """Tests that a number is adjusted for units if it can be."""
    assert _adjust_units(number, units) == expected_number
