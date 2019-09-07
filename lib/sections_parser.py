import osmium
import json
from lib.parser import Parser

class SectionsParser(Parser):
    def __init__(self, features):
        super().__init__(features)
        self._relations_dict = {}

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

        # We grab the line/system data
        for line_info in props['lines']:
            name = line_info['line']
            if line_info['system']:
                name = line_info['system'] + ' ' + name
            if not name in self._relations_dict:
                self._relations_dict[name] = []
            self._relations_dict[name].append(id)

        # We set the tags
        tags = [('citylines:id', str(props['id']))]
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

    def load_relations(self):
        for i, rel_name in enumerate(self._relations_dict):
            rel = self._relations_dict[rel_name]
            tags = [('name',rel_name)]
            members = []
            for way_id in rel:
                members.append(('w', way_id,''))
            rel = osmium.osm.mutable.Relation(id=-(i+1),members=members,tags=tags)
            self._relations.append(rel)

    def node_id(self):
        return -(len(self.nodes) + 1)

