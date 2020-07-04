from internet_model import Page, Internet

# Credit for this script goes to:
# https://github.com/UPstartDeveloper/Graph-ADT/blob/master/util/file_reader.py


def read_graph_from_file(filename):
    """Read in data from the specified filename,
       and returns an Internet object corresponding
       to that data.

       Parameters:
       filename (str): The relative path of the file to be processed

       Returns:
       Internet: A directed, weighted graph containing the specified
                 Pages. Not necessarily connected.

    """
        # Open the file
    with open(filename) as f:
        # read in all lines from the file, without the '\n' characters
        lines = [line[:-1] for line in f.readlines()]
        internet = Internet()
        # Use the 1st line to add the vertices
        page_ids = lines[0].split(',')
        for p_id in page_ids:
            internet.add_page_by_id(p_id)
        # Use the 2nd+ line to add the edges
        for index, line in enumerate(lines):
            if index >= 1:
                # get ids of the vertices
                ids = line[1:4].split(',')
                # add an edge from the first vertex to the second
                page1, page2 = ids[0], ids[1]
                internet.link_pages(page1, page2)
        # Return the Graph
        return internet

if __name__ == '__main__':
    filename = 'test_files/small_input.txt'
    internet = read_graph_from_file(filename)
    print(internet)
