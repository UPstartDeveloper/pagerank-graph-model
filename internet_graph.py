import math
import numpy as np
from collections import deque


class PageVertex:
    """
    Representation of a single web page and its linked pages.
    """
    def __init__(self, id):
        """Initialize attributes of a new PageVertex instance."""
        self.page_id = id
        # map each linked page_id --> PageVertex obj
        self.neighbors = dict()
        # each link has the same weight
        self.link_weight = 0

    def __set_link_weight(self, num_links=None):
        """Adjust the weight of any PageVertex linked by this
           instance to be the inverse of its number of
           neighbors.

        """
        if num_links is None:
          num_links = len(self.neighbors)
        self.link_weight = 1 / num_links

    def add_link(self, page):
        '''Link another PageVertex from this instance.'''
        # recalculate the link weight
        num_links = 1 + len(self.neighbors)
        self.__set_link_weight(num_links)
        # add neighbor
        self.neighbors[page.get_id()] = page

    def __str__(self):
        '''Output the PageVertex and its linked neighbors.'''
        neighbor_ids = list(self.neighbors.keys())
        return f'{self.page_id} adjacent to {neighbor_ids}'

    def __repr__(self):
        '''Output the list of neighbors of this PageVertex.'''
        return self.__str__()

    def get_neighbors(self):
        """Return the PageVertex instances that are linked by 
           this instance.
           
        """
        return list(self.neighbors.values())

    def get_neighbors_with_weights(self):
        """Return the PageVertex instances that are linked by 
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


class InternetGraph:
    """
    Represents a composition of all PageVertex instances
    in the network. Is a directed, weighted, and 
    not neccessarily connected graph.

    Notes on PageVertexRank algorithm, from Zach Starr video:
    - the weight of each edge = 1 / # neighbors of a PageVertex
    - each page only knows about the links it gives out,
       and not endorsements that link to it
    - using iteration we can create an adjacency matrix
      to show
      (in each column): the endorsements given out by each
                        PageVertex, and
      (in each row): we show the endorsements that each PageVertex
                     receives

    """
    def __init__(self):
        '''Construct a new InternetGraph instance.'''
        # map each page_id --> PageVertex obj
        self.pages = dict()

    def add_page_by_id(self, page_id):
        """Instaniate a new PageVertex, then add to
           the InternetGraph.
        
        """
        self.pages[page_id] = PageVertex(page_id)

    def add_page_by_obj(self, page):
        """Add a PageVertex instance into the collection
           of all PageVertex instances.
        
        """
        self.pages[page.get_id()] = page

    def get_pages(self):
        '''Return a list of all PageVertex instances.'''
        return list(self.pages.values())

    def contains_page(self, page_id):
        '''Returns True if a PageVertex exists with 'page_id'.'''
        return page_id in self.pages

    def get_page(self, page_id):
        '''Returns a PageVertex with matching page_id.'''
        # raise error, or return object
        if page_id not in self.pages:
            raise KeyError(f'PageVertex {page_id} not found.')
        return self.pages[page_id]

    def link_pages(self, page1_id, page2_id):
        '''Adds a link from PageVertex 1 to PageVertex 2.'''
        page1_obj, page2_obj = (
            self.get_page(page1_id),
            self.get_page(page2_id)
        )
        page1_obj.add_link(page2_obj)

    def __str__(self):
        '''Return the PageVertexs in this instance.'''
        return f'InternetGraph with PageVertexs: {self.get_pages()}'


    """What's the PageVertexRank rating of each page?"""

    def compute_inlink_values(self):
        """Return a dict of the total endorsement given
           to each PageVertex.

           Complexity Analysis:
           The runtime of this implementation scales quadratically
           with the size of P, the number of PageVertexs in the InternetGraph.

           It also scales with the size of L, the number of links
           in the InternetGraph, because that is the sum total of addition
           operations we will use to calculate the total endorsement 
           received by each PageVertex.
           
           This runtime can be expressed in Big O as O(P^2 + L)

        """
        # compute how much endorsement each PageVertex got
        all_page_ids = list(self.pages.keys())  # O(P)
        inlinks = dict()
        for page_id1 in all_page_ids:  # P^2 iterations
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
        for page in inlinks:  # P iterations
            total_endorsement = sum(inlinks[page])  # O(L)
            inlinks[page] = total_endorsement
        return inlinks

    def sort_pages_by_inlinks(self, inlinks):
        """Return a list of PageVertexs sorted from 
           greatest to least total endorsement values.

           Complexity Analysis:
           The runtime of this method scales asymptotically 
           the the time taken to sort the pages from greatest to
           least. Since this step of the process is quadratically 
           dependent on P, the number of PageVertexs, this can be expressed 
           as O(P^2).

        """
        # rank all the PageVertexs
        highest_rank_values = sorted(inlinks.values())  # O(P log P)
        highest_rank_pages = list()
        # sort pages from greatest to least
        while len(highest_rank_values) > 0:  # P iterations
            highest_val = max(highest_rank_values)  # O(P)
            # find the page matching the next highest value
            for page in inlinks:  # P iterations
                if inlinks[page] == highest_val:
                    highest_rank_pages.append(page)
                    # remove the value from the list
                    highest_rank_values.remove(highest_val)  # O(P)
        return highest_rank_pages

    def bucket_ranked_pages(self, highest_rank_pages):
        """Return a list of tuples for each PageVertex,
           along with its PageVertexRank rating.

           Complexity Analysis:
           The runtime of this method scales linearly with the size
           of P, as P grows asympotitcally larger. Therefore, the Big O
           notation of the runtime is O(P).

        """
        # convert to list of PageVertexRank ratings
        rankings = list()
        # store variables for number of pages to rank, and 
        # ratings we can give out (scale 1-10)
        num_rankings, num_possible_ranks = len(highest_rank_pages), 10  # O(P)
        if num_rankings < num_possible_ranks:
            # each PR up to 10 is each to the index
            for index, page in enumerate(highest_rank_pages):  # O(P)
                rankings.append((page, index + 1))
        else:
            # each page is assigned a PR according to buckets
            bucket_len = math.ceil(num_rankings / num_possible_ranks)  # O(1)
            for index, page in enumerate(highest_rank_pages):  # P iterations
                rating = int(index / bucket_len) + 1
                rankings.append((page, rating))  # O(P) amortized
        return rankings

    def rank_pages(self):
        """
        Return the PageVertexRank rating for each page.

        Complexity Analysis:
        The runtime of this method grows in relation to P and L
        asymptotically, which represent the number of PageVertexs and the 
        total number of links in the InternetGraph respectively. The Big O
        notation for the combined runtime of the three helper methods
        would be O(P^2 + L).

        """
        # compute how much endorsement each PageVertex got
        inlinks = self.compute_inlink_values()  # O(P^2 + L)
        # rank all the PageVertexs
        highest_rank_pages = self.sort_pages_by_inlinks(inlinks)  # O(P^2)
        # convert to list of PageVertexRank ratings
        rankings = self.bucket_ranked_pages(highest_rank_pages)  # O(P)
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
        start_id (str): The id of the start PageVertex.
        link_distance (int): The distance from the 
                                start vertex we want

        Returns:
        List<str>: All PageVertex ids that are 'link_distance' away

        Complexity Analysis:
        This function attempts to process each PageVertex, by way of 
        each link in the InternetGraph. It scales in linear proportion to 
        P and L as they grow asymptotically larger, therefore
        the Big O notation of this function is O(P + L).

        """
        # check to make sure we have a valid start_id
        if not self.contains_page(start_id):
            raise KeyError(f"PageVertex {start_id} not found in the InternetGraph!")
        # Store the starting page in a variable 
        start_page_obj = self.get_page(start_id)
        # Keep a count of steps taken from start so far
        steps = -1
        # Keep a dict of PageVertex ids, mapped to their distance from start
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
                # add the current PageVertex to the dict
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

    """What's the Shortest Weighted Path Between 2 PageVertexs (by links)?"""

    def find_shortest_path(self, start_id, target_id):
        """
        Use Dijkstra's Algorithm to return the total weight
        of the shortest path from a start page 
        to a destination.

        Complexity Analysis:
        The runtime of this method asymptotically increases quadratically 
        with respect to P, the number of PageVertexs. The longest step is finding 
        the minimum PageVertex to add, since an ordinary array is currently used to
        simulate using a binary min heap.

        Overall, the runtime of this method is O(P^2).

        """
        # Check that both start and target PageVertexs valid
        if self.contains_page(start_id) is False:  # O(P)
            raise KeyError(f'{start_id} not found in InternetGraph!')
        elif self.contains_page(target_id) is False:  # O(P)
            raise KeyError(f'{target_id} not found in InternetGraph!')
        # A: initialize all page distances to INFINITY away
        page_weight = dict()  # O(1)
        for page_obj in self.pages.values():  # P iterations
            page_weight[page_obj] = float('inf')
        # B: Calculate Shortest Paths from Start PageVertex
        start_page = self.pages[start_id]  # O(1)
        page_weight[start_page] = 0
        while len(list(page_weight.items())) > 0:  # P iterations
            # Get the minimum-distance remaining PageVertex
            min_distance = min(list(page_weight.values()))  # O(P)
            min_page = None
            # find the minumum-weighted PageVertex
            for page in page_weight:  # P iterations
                if page_weight[page] == min_distance:
                    min_page = page
            # If target found, return its distance
            if min_page.page_id == target_id:
                return page_weight[min_page]
            # B: List the PageVertex's neighbors
            neighbor_weights = min_page.get_neighbors_with_weights()  # O(L)
            # C: Update the PageVertex's neighbors
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
    # A: instaniate the PageVertexs and Graph
    pageA = PageVertex('A')
    pageB = PageVertex('B')
    pageC = PageVertex('C')
    pageD = PageVertex('D')
    pageA.add_link(pageB)
    pageB.add_link(pageC) 
    pageB.add_link(pageD)
    pageC.add_link(pageA)
    pageC.add_link(pageD)
    pageD.add_link(pageA)
    pageD.add_link(pageB)
    internet = InternetGraph()
    internet.add_page_by_obj(pageA)
    internet.add_page_by_obj(pageB)
    internet.add_page_by_obj(pageC)
    internet.add_page_by_obj(pageD)
    # B: Test PageVertexRank
    rankings = internet.rank_pages()
    print(f'Final rankings: {rankings}')
    # C: Seeing What PageVertexs Can be Reached from 'B'
    neighbors = internet.find_pages_n_away('B', 2)
    print('Shortest distance neighbors 2 links away ' +
          f'from B: {neighbors}')
    # D: Finding Length of Shortest Path
    b_to_d = internet.find_shortest_path('B', 'D')
    print(f'Minimum weight of path from B to D: {b_to_d}')


