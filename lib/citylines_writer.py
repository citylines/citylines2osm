import osmium

class CitylinesWriter(object):
    def __init__(self, output, features):
        self.features = features
        self.writer = osmium.SimpleWriter(output)
        self._nodes = 0

    def call(self):
        for feature in self.features:
            props = feature['properties']
            coordinates = feature['geometry']['coordinates']
            self.load_nodes(coordinates)

    def load_nodes(self, coordinates):
        for lonlat in coordinates:
            location = osmium.osm.Location(lonlat[0], lonlat[1])
            node = osmium.osm.mutable.Node(id=self.node_id(), location=location)
            self.writer.add_node(node)

    def node_id(self):
        self._nodes += 1
        return -self._nodes
