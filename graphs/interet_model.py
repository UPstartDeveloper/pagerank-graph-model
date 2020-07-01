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

    def __set_link_weight(self, num_links=len(self.neighbors)):
        """Adjust the weight of any Page linked by this instance
           to be the inverse of its number of neighbors.

        """
        self.link_weight = 1 / num_links

    def add_link(self, page):
        # recalculate the link weight
        num_links = 1 + len(self.neighbors)
        self.set_link_weight(num_links)
        # add neighbor
        self.neighbors[page.id] = page

    def __str__(self):
        """Output the Page and its linked neighbors."""
        neighbor_ids = list(self.neighbors.keys())
        return f'{self.id} adjacent to {neighbor_ids}'

    def __repr__(self):
        """Output the list of neighbors of this Page."""
        return self.__str__()

    def get_neighbors(self):
        """Return the Page instances that are linked by 
           this instance.
           
        """
        return list(self.neighbors.values())

    def get_id(self):
        """Return the id of this vertex."""
        return self.id


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
        """Construct a new Internet instance."""
        # map each page_id --> Page obj
        self.pages = dict()

    def add_page(self, page_obj):
        """Add a Page instance into the collection
           of all Page instances.
        
        """
        self.pages[page_obj.get_id()] = page_obj

    def get_pages(self):
        """Return a list of all Page instances."""
        return list(self.pages.values())

    def rank_pages(self):
        """
        Return the PageRank rating for each page.
        """
        # create a top-level dictionary of page rankings
        rankings = dict()
        all_page_ids = list(self.pages.keys())
        # set default values - either 0 (for a Page to itself) or infinity
        for page1 in all_page_ids:
            dist[page1] = dict()
            for page2 in all_page_ids:
                dist[page1][page2] = float('inf')
            rankings[page1][page1] = 0
        # add all outlinks to the dictionary
        all_page_objs = self.get_pages()
        for page in all_page_objs:
            linked_pages = page.get_neighbors()
            for neighbor in linked_pages:
                rankings[page.get_id()][neighbor.get_id()] = page.link_weight
        """# execute the algorithm - "relax" the distances using an intermediate vertex
        for k in all_page_ids:
            for i in all_page_ids:
                for j in all_page_ids:
                    rankings[i][j] = (
                        min(rankings[i][j], rankings[i][k] + rankings[k][j])
                    )"""
        # compute how much endorsement each Page got
        # rank all the Pages
        return rankings


