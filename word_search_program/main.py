"""This runs the program that finds the largest number in a PDF file."""

import sys
import pdfplumber
from word_search_program.page_reader import process_page


def get_file_name():
    if len(sys.argv) <= 1:
        raise ValueError("Expected a file name to be passed to this python module.")
    if len(sys.argv) > 2:
        raise ValueError("Expected only one PDF to be searched at a time.")
    return sys.argv[1]


print("Searching file:", get_file_name())

pdf = pdfplumber.open(get_file_name())

largest_number = 0
for page in pdf.pages:
    page_result = process_page(page)
    if page_result > largest_number:
        largest_number = page_result

print(f"Largest number found: {largest_number}")
