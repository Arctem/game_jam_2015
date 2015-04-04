class Decoration:
    def __init__(self, name, keywords, attributes=[], short_desc=None, desc=None):
        self.name = name
        self.short_desc = short_desc
        self.keywords = keywords
        self.attributes = attributes
        self.desc = desc
        self.room = None

    def short_description(self):
        return self.short_desc

    def description(self):
        return self.desc