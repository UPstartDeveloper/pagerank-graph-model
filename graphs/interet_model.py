import math
import numpy as np


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
        """Adjust the weight of any Page linked by this instance
           to be the inverse of its number of neighbors.

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
        return f'{self.id} adjacent to {neighbor_ids}'

    def __repr__(self):
        '''Output the list of neighbors of this Page.'''
        return self.__str__()

    def get_neighbors(self):
        """Return the Page instances that are linked by 
           this instance.
           
        """
        return list(self.neighbors.values())

    def get_id(self):
        """Return the id of this vertex."""
        return self.page_id


class Internet:
    """
    Represents a composition of all Page instances in the network.

    Notes on PageRank algorithm, from Zach Starr video:
    - the weight of each edge = 1 / # neighbors of a Page
    - each page only knows about the links it gives out, and not 
      endorsements that link to it
    - using iteration we can create an adjacency matrix to show
      (in each column) the endorsements given out by each Page, and
      (in each row) we show the endorsements that each Page receives

    """
    def __init__(self):
        '''Construct a new Internet instance.'''
        # map each page_id --> Page obj
        self.pages = dict()

    def add_page(self, page_obj):
        """Add a Page instance into the collection
           of all Page instances.
        
        """
        self.pages[page_obj.get_id()] = page_obj

    def get_pages(self):
        '''Return a list of all Page instances.'''
        return list(self.pages.values())

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
                # use outlinks to see endorsements from other pages
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


if __name__ == "__main__":
    # Test Page Ranking Function on Connected Interet Graph

    # A: instaniate the Pages
    pageA = Page('A')
    pageB = Page('B')
    pageC = Page('C')
    pageD = Page('D')
    # B: add links between Pages
    pageA.add_link(pageB)
    pageB.add_link(pageC) 
    pageB.add_link(pageD)
    pageC.add_link(pageA)
    pageC.add_link(pageD)
    pageD.add_link(pageA)
    pageD.add_link(pageB)
    # C: Add Pages to an Internet
    internet = Internet()
    internet.add_page(pageA)
    internet.add_page(pageB)
    internet.add_page(pageC)
    internet.add_page(pageD)
    # D: Test Algorithm
    rankings = internet.rank_pages()
    # print(f'Inlinks: {inlinks}')
    print(f'Final rankings: {rankings}')


