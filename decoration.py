class Decoration:
    def __init__(self, name, desc=None):
        self.name = name
        self.desc = desc

    def description(self):
        return self.desc