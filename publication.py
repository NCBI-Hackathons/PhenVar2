class Publication():
    def __init__(self, id, title, abstract, rsids=[]):
        self.id = id
        self.title = title
        self.abstract = abstract
        self.rsids = rsids