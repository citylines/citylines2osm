import osmium

class CitylinesWriter(object):
    def __init__(self, output, features):
        self.features = features
        self.writer = osmium.SimpleWriter(output)
        self._nodes = 0

    def call(self):
        ways = []
        for feature in self.features:
            props = feature['properties']
            coordinates = feature['geometry']['coordinates']
            ref_ids = self.load_nodes(coordinates)
            ways.append(osmium.osm.mutable.Way(id=-props['id'], nodes=ref_ids))
        for way in ways:
            self.writer.add_way(way)

    def load_nodes(self, coordinates):
        refs = []
        for lonlat in coordinates:
            location = osmium.osm.Location(lonlat[0], lonlat[1])
            id = self.node_id()
            refs.append(id)
            node = osmium.osm.mutable.Node(id=id, location=location)
            self.writer.add_node(node)
        return refs

    def node_id(self):
        self._nodes += 1
        return -self._nodes
