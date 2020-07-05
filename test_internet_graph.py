import unittest
from internet_graph import PageVertex, InternetGraph
import file_reader


class TestInternetGraphSmallInput(unittest.TestCase):
    """
    Test suite for datasets of under 30 PageVertexs.
    """
    def test_rank_pages_small(self):
        '''Test the PageRank ratings given for test input file.'''
        internet = file_reader.read_graph_from_file(
            'test_files/small_input.txt'
        )
        actual = internet.rank_pages()
        expected = [
            ('B', 1),
            ('C', 2),
            ('D', 3),
            ('A', 4),    
        ]
        self.assertEqual(actual, expected)

    def test_find_n_away(self):
        '''Test neighbors found given a certain distance.'''
        internet = file_reader.read_graph_from_file(
            'test_files/small_input.txt'
        )
        start_id, links = 'B', 2
        actual = internet.find_pages_n_away(start_id, links)
        expected = ['A']
        self.assertEqual(actual, expected)

    def test_shortest_path(self):
        '''Test the calculated total weight of shortest path.'''
        internet = file_reader.read_graph_from_file(
            'test_files/small_input.txt'
        )
        start, target = 'B', 'D'
        actual = internet.find_shortest_path(start, target)
        expected = 0.5
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()