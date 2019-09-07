import osmium
import json

class FeaturesParser(object):
    def __init__(self, features, exclude_osm_elements=False):
        self.features = features
        self._nodes = []
        self._ways = []
        self._relations = []
        self._relations_dict = {}
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
            tags = [('name',rel_name)]
            members = []
            for m in rel:
                members.append((m['type'], m['id'],''))
            rel = osmium.osm.mutable.Relation(id=-(i+1),members=members,tags=tags)
            self._relations.append(rel)

    def _load_feature(self, feature):
        props = feature['properties']
        way = props['klass'] == 'Section'

        id = props['osm_id'] if 'osm_id' in props else None
        refs = []

        if id and self.exclude_osm_elements:
            return

        if not id:
            id = -props['id']
            if way:
                refs = self._load_nodes(feature['geometry']['coordinates'])

        self._extract_lines(id, way, props)
        tags = self._build_tags(props)

        if way:
            self._ways.append(osmium.osm.mutable.Way(id=id, nodes=refs, tags=tags))
        else:
            if not 'name' in dict(tags):
                tags.append(('name', props['name']))
            lonlat = feature['geometry']['coordinates']
            self._nodes.append(osmium.osm.mutable.Node(id=id, location=lonlat, tags=tags))

    def _load_nodes(self, coordinates):
        refs = []
        for lonlat in coordinates:
            id = -(len(self.nodes) + 1)
            refs.append(id)
            self._nodes.append(osmium.osm.mutable.Node(id=id, location=lonlat))
        return refs

    def _build_tags(self, props):
        tags = [('citylines:id', str(props['id']))]
        if 'osm_tags' in props:
            original_tags = json.loads(props['osm_tags'])
            for key in original_tags:
                tags.append((key, str(original_tags[key])))
        return tags

    def _extract_lines(self, id, way, props):
        for line_info in props['lines']:
            name = line_info['line']
            if line_info['system']:
                name = line_info['system'] + ' ' + name
            if not name in self._relations_dict:
                self._relations_dict[name] = []
            t = 'w' if way else 'n'
            self._relations_dict[name].append({'id':id, 'type':t})
