class Item:
    def __init__(self, name, short_desc, desc, keywords, attributes=[]):
        self.name = name
        self.short_desc = short_desc
        self.keywords = keywords
        self.attributes = attributes
        for attr in self.attributes:
            attr.parent = self
        self.desc = desc
        self.room = None
        self.player = None

    def short_description(self):
        return self.short_desc

    def description(self):
        return self.desc
