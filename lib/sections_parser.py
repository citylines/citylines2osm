import osmium
import json
from lib.parser import Parser

class SectionsParser(Parser):
    def run(self):
        self.load_ways()
        self.load_relations()

    def load_ways(self):
        for feature in self.features:
            self._ways.append(self.build_way(feature))

    def build_way(self, feature):
        props = feature['properties']

        id = props['osm_id']
        refs = []

        if not id:
            id = -props['id']
            refs = self.load_nodes(feature['geometry']['coordinates'])

        self._extract_lines(id, props)

        return osmium.osm.mutable.Way(id=id, nodes=refs, tags=self._build_tags(props))

    def load_nodes(self, coordinates):
        refs = []
        for lonlat in coordinates:
            id = self._node_id()
            refs.append(id)
            self._nodes.append(osmium.osm.mutable.Node(id=id, location=lonlat))
        return refs

    def _node_id(self):
        return -(len(self.nodes) + 1)

    def _member_type(self):
        return 'w'
