class Unit:
    id=None
    shortDesc=None
    longDesc=None
    active=None

    def __init__(self, shortDesc, longDesc, id=None, active=False):
        self.id = id
        self.shortDesc = shortDesc
        self.longDesc = longDesc
        self.active = active