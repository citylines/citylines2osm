import osmium
import json

class SectionsParser(object):
    def __init__(self, features):
        self.features = features
        self._nodes = []
        self._ways = []
        self.load_features()

    @property
    def nodes(self):
        return self._nodes

    @property
    def ways(self):
        return self._ways

    def load_features(self):
        for feature in self.features:
            self._ways.append(self.build_way(feature))

    def build_way(self, feature):
        props = feature['properties']
        coordinates = feature['geometry']['coordinates']

        id = props['osm_id']
        refs = []

        if not id:
            id = -props['id']
            refs = self.load_nodes(coordinates)

        tags = []
        tags.append(('citylines:id', str(props['id'])))
        if 'osm_tags' in props:
            original_tags = json.loads(props['osm_tags'])
            for key in original_tags:
                tags.append((key, str(original_tags[key])))

        return osmium.osm.mutable.Way(id=id, nodes=refs, tags=tags)

    def load_nodes(self, coordinates):
        refs = []
        for lonlat in coordinates:
            id = self.node_id()
            refs.append(id)
            self._nodes.append(osmium.osm.mutable.Node(id=id, location=lonlat))
        return refs

    def node_id(self):
        return -(len(self.nodes) + 1)

