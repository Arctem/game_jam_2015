class Connection:
    def __init__(self, origin, destination, desc=None, pass_desc=None,
            locked = False):
        self.origin = origin
        self.destination = destination
        self.desc = desc
        self.pass_desc = pass_desc
        self.locked = locked

    def short_description(self):
        return self.short_desc

    def description(self):
        return self.desc