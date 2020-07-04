import unittest
from internet_graph import Page, Internet
import file_reader


if __name__ == "__main__":
    internet = (
        file_reader.read_graph_from_file(
            'test_files/small_input.txt'
        )
    )