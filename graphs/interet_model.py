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

class Internet:
    """
    Represents a composition of all Page instances in the network.
    """
    def __init__(self):
        # map each page_id --> Page obj
        self.pages = dict()