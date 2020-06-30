class Page:
    """
    Representation of a single web page and its linked pages.
    """
    def __init__(self, id):
        self.page_id = id
        # map each linked page_id --> Page obj
        self.neighbors = dict()
        # each link has the same weight
        self.link_weight = 0

    def __set_link_weight(self, num_links=len(self.neighbors)):
        self.link_weight = 1 / num_links

    def add_link(self, page):
        # recalculate the link weight
        num_links = 1 + len(self.neighbors)
        self.set_link_weight(num_links)
        # add neighbor
        self.neighbors[page.id] = page

class Internet:
    """
    Represents a composition of all Page instances in the network.
    """
    def __init__(self):
        # map each page_id --> Page obj
        self.pages = dict()