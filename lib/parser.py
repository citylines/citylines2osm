class Parser(object):
    def __init__(self, features):
        self.features = features
        self._nodes = []
        self._ways = []
        self._relations = []

    @property
    def nodes(self):
        return self._nodes

    @property
    def ways(self):
        return self._ways

    @property
    def relations(self):
        return self._relations

    def run(self):
        raise NotImplementedError
