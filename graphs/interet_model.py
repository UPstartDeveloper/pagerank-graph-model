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
    """
    def __init__(self):
        # map each page_id --> Page obj
        self.pages = dict()