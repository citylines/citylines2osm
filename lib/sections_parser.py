import osmium

class SectionsParser(object):
    def __init__(self, features):
        self.features = features
        self.nodes = []
        self.ways = []
        self.load_features()

    def load_features(self):
        for feature in self.features:
            props = feature['properties']
            coordinates = feature['geometry']['coordinates']
            refs = self.load_nodes(coordinates)
            self.ways.append(osmium.osm.mutable.Way(id=-props['id'], nodes=refs))

    def load_nodes(self, coordinates):
        refs = []
        for lonlat in coordinates:
            id = self.node_id()
            refs.append(id)
            self.nodes.append(osmium.osm.mutable.Node(id=id, location=lonlat))
        return refs

    def node_id(self):
        return -(len(self.nodes) + 1)

