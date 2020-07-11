import unittest
from internet_graph import PageVertex, InternetGraph
import file_reader


class TestFileReader(unittest.TestCase):
        def test_read_graph_from_file(self):
            """
            An InternetGraph is constructed based off reading from a 
            file of the PageVertices and their links.
            """
            internet = file_reader.read_graph_from_file(
                'test_files/small_input.txt'
            )
            # test number of PageVertices creates
            self.assertEqual(len(internet.pages), 4)
            # test the links created
            pageA, pageB, pageC, pageD = (
                internet.get_page('A'),
                internet.get_page('B'),
                internet.get_page('C'),
                internet.get_page('D')
            )
            self.assertTrue(pageA.has_neighbor('B'))
            self.assertTrue(pageB.has_neighbor('C'))
            self.assertTrue(pageB.has_neighbor('D'))
            self.assertTrue(pageC.has_neighbor('A'))
            self.assertTrue(pageC.has_neighbor('D'))
            self.assertTrue(pageD.has_neighbor('A'))
            self.assertTrue(pageD.has_neighbor('B'))

        def test_read_graph_from_file_no_newline(self):
            """
            The file reader function throws an error if
            there is no newline at the end of the file.
            """
            with self.assertRaises(RuntimeError):
                file_reader.read_graph_from_file(
                    'test_files/error_input1.txt'
                    )

        def test_read_graph_from_file_extra_comma(self):
            """
            The file reader function throws an error if
            a PageVertex is instaniated with '' as its
            id.
            """
            with self.assertRaises(AssertionError):
                file_reader.read_graph_from_file(
                    'test_files/error_input2.txt'
                    )


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