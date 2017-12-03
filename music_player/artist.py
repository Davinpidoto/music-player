class Artist:

    def __init__(self, id, name, albums):
        self.id = id
        self.name = name
        self.albums = albums

    def json_default(self):
        return self.__json__()
