from lib.elements import Node, Way, Relation

class FeaturesParser(object):
    def __init__(self, features, transport_modes_provider, exclude_osm_elements=False):
        self.features = features
        self._nodes = []
        self._ways = []
        self._relations = []
        self._relations_dict = {}
        self._transport_modes_provider = transport_modes_provider
        self.exclude_osm_elements = exclude_osm_elements

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
        self.load_features()
        self.load_relations()

    def load_features(self):
        for feature in self.features:
            self._load_feature(feature)

    def load_relations(self):
        for i, rel_name in enumerate(self._relations_dict):
            rel = self._relations_dict[rel_name]
            relation = Relation(self._transport_modes_provider, {**{'id':-(i+1),'name':rel_name},**rel})
            self._relations.append(relation.osmium_object())

    def _load_feature(self, feature):
        if feature['properties']['klass'] == 'Section':
            way = Way(feature, self._transport_modes_provider, nodes_count=len(self._nodes))
            if way.osm_id and self.exclude_osm_elements:
                return
            self._extract_lines(way)
            self._nodes += way.nodes()
            self._ways.append(way.osmium_object())
        else:
            node = Node(feature, self._transport_modes_provider)
            if node.osm_id and self.exclude_osm_elements:
                return
            self._extract_lines(node)
            self._nodes.append(node.osmium_object())


    def _extract_lines(self, el):
        for line in el.lines_info():
            name = line['name']
            if not name in self._relations_dict:
                self._relations_dict[name] = {'url_name': line['url_name'], 'members': []}
            self._relations_dict[name]['members'].append(el.member())
