import unittest
from internet_graph import PageVertex, InternetGraph
import file_reader


class TestInternetGraphSmallInput(unittest.TestCase):
    """
    Test suite for datasets of under 10 PageVertices.
    """
    def test_rank_pages_small(self):
        '''Test the PageRank ratings given for small test input file.'''
        internet = file_reader.read_graph_from_file(
            'test_files/small_input.txt'
        )
        actual = internet.rank_pages()
        expected = [
            ('B', 1),
            ('D', 2),
            ('A', 3),
            ('C', 4)
        ]
        self.assertEqual(actual, expected)

    def test_find_n_away(self):
        """
        Test neighbors found given a certain minimum distance away from a
        startinmg vertex.
        """
        internet = file_reader.read_graph_from_file(
            'test_files/small_input.txt'
        )
        start_id, links = 'B', 2
        actual = internet.find_pages_n_away(start_id, links)
        expected = ['A']
        self.assertEqual(actual, expected)

    def test_shortest_path(self):
        """
        Test the calculated total weight of shortest path
        between two PageVertices.
        """
        internet = file_reader.read_graph_from_file(
            'test_files/small_input.txt'
        )
        start, target = 'B', 'D'
        actual = internet.find_shortest_path(start, target)
        expected = 0.5
        self.assertEqual(actual, expected)


class TestInternetGraphLargeInput(unittest.TestCase):
    """
    Test suite for datasets of over 10 PageVertices.
    Includes edge cases such as having multiple 
    connected components.
    """
    def test_rank_pages_large(self):
        '''Test the PageRank ratings given for large test input file.'''
        internet = file_reader.read_graph_from_file(
            'test_files/large_input.txt'
        )
        actual = internet.rank_pages()
        expected = [
            ('H', 1),
            ('F', 1),
            ('C', 2),
            ('D', 2),
            ('B', 3),
            ('E', 3),
            ('E', 4), 
            ('G', 4),
            ('K', 5),
            ('K', 5),
            ('K', 6)
        ]
        self.assertEqual(actual, expected)

    def test_find_n_away(self):
        """
        Test neighbors found given a certain minimum distance away from a
        startinmg vertex.
        """
        internet = file_reader.read_graph_from_file(
            'test_files/large_input.txt'
        )
        start_id, links = 'B', 2
        actual = internet.find_pages_n_away(start_id, links)
        expected = ['A', 'F', 'E', 'G', 'H']
        self.assertEqual(actual, expected)

    def test_shortest_path(self):
        """
        Test the calculated total weight of shortest path
        between two PageVertices.
        """
        internet = file_reader.read_graph_from_file(
            'test_files/large_input.txt'
        )
        start, target = 'B', 'D'
        actual = internet.find_shortest_path(start, target)
        expected = 0.2
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()