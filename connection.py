class Connection:
    def __init__(self, origin, destination, short_desc, desc, pass_desc,
            keywords, attributes=[], locked=False, locked_desc=None):
        self.origin = origin
        self.destination = destination
        self.keywords = keywords
        self.desc = desc
        self.short_desc = short_desc
        self.pass_desc = pass_desc
        self.attributes = attributes
        for attr in self.attributes:
            attr.parent = self
        self.locked = locked
        self.locked_desc = locked_desc

    def short_description(self):
        return self.short_desc

    def description(self):
        return self.desc