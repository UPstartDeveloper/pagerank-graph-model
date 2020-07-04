import math
import numpy as np
from collections import deque
from utils import file_reader


class Page:
    """
    Representation of a single web page and its linked pages.
    """
    def __init__(self, id):
        """Initialize attributes of a new Page instance."""
        self.page_id = id
        # map each linked page_id --> Page obj
        self.neighbors = dict()
        # each link has the same weight
        self.link_weight = 0

    def __set_link_weight(self, num_links=None):
        """Adjust the weight of any Page linked by this
           instance to be the inverse of its number of
           neighbors.

        """
        if num_links is None:
          num_links = len(self.neighbors)
        self.link_weight = 1 / num_links

    def add_link(self, page):
        '''Link another Page from this instance.'''
        # recalculate the link weight
        num_links = 1 + len(self.neighbors)
        self.__set_link_weight(num_links)
        # add neighbor
        self.neighbors[page.get_id()] = page

    def __str__(self):
        '''Output the Page and its linked neighbors.'''
        neighbor_ids = list(self.neighbors.keys())
        return f'{self.page_id} adjacent to {neighbor_ids}'

    def __repr__(self):
        '''Output the list of neighbors of this Page.'''
        return self.__str__()

    def get_neighbors(self):
        """Return the Page instances that are linked by 
           this instance.
           
        """
        return list(self.neighbors.values())

    def get_neighbors_with_weights(self):
        """Return the Page instances that are linked by 
           this instance, along with the weight of that
           link
           
        """
        neighbors = self.get_neighbors()
        # add each neighbir along with its weights
        neighbor_weights = list()
        for n in neighbors:
            pair = (n, n.link_weight)
            neighbor_weights.append(pair)
        return neighbor_weights

    def get_id(self):
        """Return the id of this vertex."""
        return self.page_id


class Internet:
    """
    Represents a composition of all Page instances
    in the network. Is a directed, weighted, and 
    not neccessarily connected graph.

    Notes on PageRank algorithm, from Zach Starr video:
    - the weight of each edge = 1 / # neighbors of a Page
    - each page only knows about the links it gives out,
       and not endorsements that link to it
    - using iteration we can create an adjacency matrix
      to show
      (in each column): the endorsements given out by each
                        Page, and
      (in each row): we show the endorsements that each Page
                     receives

    """
    def __init__(self):
        '''Construct a new Internet instance.'''
        # map each page_id --> Page obj
        self.pages = dict()

    def add_page_by_id(self, page_id):
        """Instaniate a new Page, then add to
           the Internet.
        
        """
        self.pages[page_id] = Page(page_id)

    def add_page_by_obj(self, page):
        """Add a Page instance into the collection
           of all Page instances.
        
        """
        self.pages[page.get_id()] = page

    def get_pages(self):
        '''Return a list of all Page instances.'''
        return list(self.pages.values())

    def contains_page(self, page_id):
        '''Returns True if a Page exists with 'page_id'.'''
        return page_id in self.pages

    def get_page(self, page_id):
        '''Returns a Page with matching page_id.'''
        # raise error, or return object
        if page_id not in self.pages:
            raise KeyError(f'Page {page_id} not found.')
        return self.pages[page_id]

    def link_pages(self, page1_id, page2_id):
        '''Adds a link from Page 1 to Page 2.'''
        page1_obj, page2_obj = (
            self.get_page(page1_id),
            self.get_page(page2_id)
        )
        page1_obj.add_link(page2_obj)

    def __str__(self):
        '''Return the Pages in this instance.'''
        return f'Internet with Pages: {self.get_pages()}'


    """What's the PageRank rating of each page?"""

    def compute_inlink_values(self):
        """Return a dict of the total endorsement given
           to each Page.

        """
        # compute how much endorsement each Page got
        all_page_ids = list(self.pages.keys())
        inlinks = dict()
        for page_id1 in all_page_ids:
            endorsements = list()
            for page_id2 in all_page_ids:
                # use outlinks to see endorsements from others
                if page_id1 == page_id2:
                    # page cannot endorse itself
                    endorsement_value = 0
                else:
                    endorsement_value = self.pages[page_id2].link_weight
                endorsements.append(endorsement_value)
            inlinks[page_id1] = endorsements
        # compute total endorsement give to each page
        for page in inlinks:
            total_endorsement = sum(inlinks[page])
            inlinks[page] = total_endorsement
        return inlinks

    def sort_pages_by_inlinks(self, inlinks):
        """Return a list of Pages sorted from 
           greatest to least total endorsement values.

        """
        # rank all the Pages
        highest_rank_values = sorted(inlinks.values())
        highest_rank_pages = list()
        # sort pages from greatest to least
        while len(highest_rank_values) > 0:
            highest_val = max(highest_rank_values)
            # find the page matching the next highest value
            for page in inlinks:
                if inlinks[page] == highest_val:
                    highest_rank_pages.append(page)
                    # remove the value from the list
                    highest_rank_values.remove(highest_val)
        return highest_rank_pages

    def bucket_ranked_pages(self, highest_rank_pages):
        """Return a list of tuples for each Page,
           along with its PageRank rating.

        """
        # convert to list of PageRank ratings
        rankings = list()
        # store variables for number of pages to rank, and 
        # ratings we can give out (scale 1-10)
        num_rankings, num_possible_ranks = len(highest_rank_pages), 10
        if num_rankings < num_possible_ranks:
            # each PR up to 10 is each to the index
            for index, page in enumerate(highest_rank_pages):
                rankings.append((page, index + 1))
        else:
            # each page is assigned a PR according to buckets
            bucket_len = math.ceil(num_rankings / num_possible_ranks)
            for index, page in enumerate(highest_rank_pages):
                rating = int(index / bucket_len) + 1
                rankings.append((page, rating))
        return rankings

    def rank_pages(self):
        """
        Return the PageRank rating for each page.
        """
        # compute how much endorsement each Page got
        inlinks = self.compute_inlink_values()
        # rank all the Pages
        highest_rank_pages = self.sort_pages_by_inlinks(inlinks)
        # convert to list of PageRank ratings
        rankings = self.bucket_ranked_pages(highest_rank_pages)
        return rankings

    """What pages can I reach N links away from this page?"""

    def find_pages_n_away(self, start_id, link_distance):
        """
        Find and return all pages n links away.
        In this implementation, if a page has multiple
        paths to it from the start that differ in distance,
        then the shortest distance is used to determine if
        should be returned or not.
        
        Arguments:
        start_id (str): The id of the start Page.
        link_distance (int): The distance from the 
                                start vertex we want

        Returns:
        List<str>: All Page ids that are 'link_distance' away 

        """
        # check to make sure we have a valid start_id
        if not self.contains_page(start_id):
            raise KeyError(f"Page {start_id} not found in the Internet!")
        # Store the starting page in a variable 
        start_page_obj = self.get_page(start_id)
        # Keep a count of steps taken from start so far
        steps = -1
        # Keep a dict of Page ids, mapped to their distance from start
        page_distances = dict()
        # queue of vertices to visit next
        queue = deque() 
        queue.append(start_page_obj)
        # Perform a BFS
        while steps < link_distance:
            # init a list of neighbors to process next
            neighbors = list()
            # Dequeue all the pages in the queue
            while len(queue) > 0:
                current_page_obj = queue.popleft()
                current_page_id = current_page_obj.get_id()
                # add the current Page to the dict
                if current_page_id not in page_distances:
                    page_distances[current_page_id] = steps + 1
                # Keep track of page to process on next iteration
                neighbors.extend(current_page_obj.get_neighbors())
            # enqueue the vertices to visit on the next iteration
            for neighbor in neighbors:
                queue.append(neighbor)
            # Increment the steps taken so far
            steps += 1
        # Return the ids of pages, target distance away
        pages_n_away = list()
        for page_id in page_distances:
            if page_distances[page_id] == link_distance:
                pages_n_away.append(page_id)
        return pages_n_away

    """What's the Shortest Weighted Path Between 2 Pages (by links)?"""

    def find_shortest_path(self, start_id, target_id):
        """
        Use Dijkstra's Algorithm to return the total weight
        of the shortest path from a start page 
        to a destination.
        """
        # Check that both start and target Pages valid
        if self.contains_page(start_id) is False:
            raise KeyError(f'{start_id} not found in Internet!')
        elif self.contains_page(target_id) is False:
            raise KeyError(f'{target_id} not found in Internet!')
        # A: initialize all page distances to INFINITY away
        page_weight = dict()
        for page_obj in self.pages.values():
            page_weight[page_obj] = float('inf')
        # B: Calculate Shortest Paths from Start Page
        start_page = self.pages[start_id]
        page_weight[start_page] = 0
        while len(list(page_weight.items())) > 0:
            # Get the minimum-distance remaining Page
            min_distance = min(list(page_weight.values()))
            min_page = None
            # find the minumum-weighted Page
            for page in page_weight:
                if page_weight[page] == min_distance:
                    min_page = page
            # If target found, return its distance
            if min_page.page_id == target_id:
                return page_weight[min_page]
            # B: List the Page's neighbors
            neighbor_weights = min_page.get_neighbors_with_weights()
            # C: Update the Page's neighbors
            for neighbor, weight in neighbor_weights:
                if neighbor in page_weight:
                    current_distance = page_weight[neighbor]
                    # Update ONLY to reduce the weight of the distance
                    new_dist = weight + page_weight[min_page]
                    if new_dist < current_distance:
                        page_weight[neighbor] = new_dist
            # remove the min weighted page from the dict
            del page_weight[min_page]


if __name__ == "__main__":
    # Runner Script
    # A: instaniate the Pages and Graph
    internet = (
        file_reader.read_graph_from_file(
            'test_files/small_input.txt'
        )
    )
    # B: Test PageRank
    rankings = internet.rank_pages()
    print(f'Final rankings: {rankings}')
    # C: Seeing What Pages Can be Reached from 'B'
    neighbors = internet.find_pages_n_away('B', 2)
    print('Shortest distance neighbors 2 links away ' +
          f'from B: {neighbors}')
    # D: Finding Length of Shortest Path
    b_to_d = internet.find_shortest_path('B', 'D')
    print(f'Minimum weight of path from B to D: {b_to_d}')


