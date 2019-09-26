import osmium
import json

class FeaturesParser(object):
    WAY = 'way'
    NODE = 'station'
    RELATION = 'relation'

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

            tags = [('name',rel_name),('type','route'),('public_transport:version','2')]

            transport_mode_tags = self._transport_mode_tags(self.RELATION, rel)
            if transport_mode_tags:
                tags.append(transport_mode_tags)

            members = []
            for m in rel['members']:
                members.append((m['type'], m['id'], m['role']))
            rel = osmium.osm.mutable.Relation(id=-(i+1),members=members,tags=tags)
            self._relations.append(rel)

    def _load_feature(self, feature):
        props = feature['properties']
        element_type = self.WAY if props['klass'] == 'Section' else self.NODE
        osm_id = props['osm_id'] if 'osm_id' in props else None

        if osm_id and self.exclude_osm_elements:
            return

        id = osm_id or -props['id']

        self._extract_lines(id, element_type, props)
        tags = self._extract_feature_tags(element_type, props)
        metadata = self._extract_feature_metadata(props)

        if element_type == self.WAY:
            refs = [] if osm_id else self._load_nodes(feature['geometry']['coordinates'])
            self._ways.append(osmium.osm.mutable.Way(id=id, nodes=refs, tags=tags, version=metadata['version']))
        else:
            lonlat = feature['geometry']['coordinates']
            self._nodes.append(osmium.osm.mutable.Node(id=id, location=lonlat, tags=tags, version=metadata['version']))

    def _load_nodes(self, coordinates):
        refs = []
        for lonlat in coordinates:
            id = -(len(self.nodes) + 1)
            refs.append(id)
            self._nodes.append(osmium.osm.mutable.Node(id=id, location=lonlat))
        return refs

    def _extract_feature_tags(self, element_type, props):
        tags = [('citylines:id', str(props['id']))]
        if 'osm_tags' in props:
            original_tags = json.loads(props['osm_tags'])
            for key in original_tags:
                tags.append((key, str(original_tags[key])))

        for line_info in props['lines']:
            if line_info['system']:
                tags.append(('network',line_info['system']))

        if element_type == self.NODE:
            if not 'name' in dict(tags):
                tags.append(('name', props['name']))
            if not 'public_transport' in dict(tags):
                tags.append(('public_transport', 'stop_position'))

        transport_mode_tags = self._transport_mode_tags(element_type, props)
        if transport_mode_tags:
            tags.append(transport_mode_tags)

        return tags

    def _extract_feature_metadata(self, props):
        metadata = {'version': None}
        if 'osm_metadata' in props:
            metadata = json.loads(props['osm_metadata'])
        return metadata

    def _extract_lines(self, id, element_type, props):
        for line_info in props['lines']:
            name = line_info['line']

            if line_info['system']:
                name = line_info['system'] + ' ' + name

            transport_mode = None # TODO

            if not name in self._relations_dict:
                self._relations_dict[name] = {'transport_mode': transport_mode, 'members': []}

            t = 'w' if element_type == self.WAY else 'n'
            role = '' if element_type == self.WAY else 'stop'

            self._relations_dict[name]['members'].append({'id':id, 'type':t, 'role': role})

    def _transport_mode_tags(self, element_type, props):
        # TODO: WAY:  set for example railway=subway
        # TODO: NODE: set for example subway=yes
        # TODO: RELATION: set for example route=subway
        return None
