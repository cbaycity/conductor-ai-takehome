To find the largest number in a pdf file, run `python word-search-program/main.py <file>` and pass in the file you're targeting to the file arguement. The program will print the largest number to the terminal.

This program should work with mulitple Python versions and limited dependencies, which are defined in the `pyproject.toml` file. If having trouble, use python 3.11.3, pip install poetry, and then run `python -m poetry shell`, `poetry install`, and then trigger the program and you should have a working environment. 

The Jupyter Notebook `program_investigation.ipynb` shows that the program was run within a correctly set up poetry environment.


Known Breaking Edge Cases:
1. The PDF has no numbers.
2. The PDF has a unit not accounted for.