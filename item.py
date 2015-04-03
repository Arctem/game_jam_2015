class Item:
    def __init__(self, name, short_desc=None, desc=None):
        self.name = name
        self.short_desc = short_desc
        self.desc = desc
        self.room = None
        self.player = None

    def short_description(self):
        return self.short_desc

    def description(self):
        return self.desc
