import osmium
import json
from lib.parser import Parser

class StationsParser(Parser):
    def run(self):
        self.load_nodes()

    def load_nodes(self):
        for feature in self.features:
            self._nodes.append(self.build_node(feature))

    def build_node(self, feature):
        props = feature['properties']

        id = props['osm_id'] or -props['id']
        lonlat = feature['geometry']['coordinates']

        return osmium.osm.mutable.Node(id=id, location=lonlat, tags=self._tags(props))

    def _tags(self, props):
        tags = super()._tags(props)
        if not 'name' in dict(tags):
            tags.append(('name', props['name']))
        return tags
