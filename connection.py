class Connection:
    def __init__(self, origin, destination, keywords, desc, short_desc,
            pass_desc, locked=False, locked_desc=None):
        self.origin = origin
        self.destination = destination
        self.keywords = keywords
        self.desc = desc
        self.short_desc = short_desc
        self.pass_desc = pass_desc
        self.locked = locked
        self.locked_desc = locked_desc

    def short_description(self):
        return self.short_desc

    def description(self):
        return self.desc