from core.pygraph.classes.digraph import digraph

from internet_graph import PageVertex, InternetGraph


def read_internet_graph(filename):
    """Read in data from the specified filename,
       and returns an InternetGraph object corresponding
       to that data.

       Special thanks to Meredith Murphy for providing starter code
       for this function.

       Parameters:
       filename (str): The relative path of the file to be processed

       Returns:
       InternetGraph: A directed, weighted graph containing the specified
                 PageVertexs. Not necessarily connected.

    """
        # Open the file
    with open(filename) as f:
        # read in all lines from the file, without the '\n' characters
        lines = [line[:-1] for line in f.readlines()]
        internet = InternetGraph()
        # Use the 1st line to add the vertices
        page_ids = lines[0].split(',')
        for p_id in page_ids:
            # check that the PageVertex id isn't empty
            assert len(p_id) != 0, (
                "Please check that you have no extra commas in the file."
            )
            # add the new PageVertex object
            internet.add_page_by_id(p_id)
        # Use the 2nd+ line to add the edges
        for index, line in enumerate(lines):
            if index >= 1:
                # get ids of the vertices
                ids = line.split(',')
                # check to make sure all the links have 2 PageVertices
                if len(ids) != 2 or '' in ids:
                    raise RuntimeError(
                    "Please check that all links have two PageVertices " + 
                    "exactly, and there is a blank line at the end of the " +
                    "file."
                )
                # check to make sure the ids are valid
                page_id1, page_id2 = ids[0], ids[1]
                if not page_id1 in internet.pages:
                    raise KeyError(f'{page_id1} not valid')
                elif not page_id2 in internet.pages:
                    raise KeyError(f'{page_id2} not valid')
                # add an edge from the first vertex to the second
                internet.link_pages(page_id1, page_id2)
        # Return the Graph
        return internet


def read_pygraph(filename):
    """Read in data from the specified filename,
       and returns an InternetGraph object corresponding
       to that data.

       Parameters:
       filename (str): The relative path of the file to be processed

       Returns:
       InternetGraph: A directed, weighted graph containing the specified
                 PageVertexs. Not necessarily connected.

    """

if __name__ == '__main__':
    graph = digraph()
    filename = 'test_files/extra_large_input.txt'
    internet = read_internet_graph(filename)
    print(f'The Internet as We Know: {internet}')
    # Test PageRank
    rankings = internet.rank_pages()
    print(f'Final rankings: {rankings}')
    # Seeing What PageVertexs Can be Reached from 'B'
    neighbors = internet.find_pages_n_away('B', 2)
    print('Shortest distance neighbors 2 links away ' +
          f'from B: {neighbors}')
    # Finding Length of Shortest Path
    b_to_d = internet.find_shortest_path('B', 'D')
    print(f'Minimum weight of path from B to D: {b_to_d}')

