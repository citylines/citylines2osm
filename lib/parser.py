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
            tags = [('name',rel_name),('type','route'),('public_transport:version','2')]
            members = []
            for m in rel:
                members.append((m['type'], m['id'], m['role']))
            rel = osmium.osm.mutable.Relation(id=-(i+1),members=members,tags=tags)
            self._relations.append(rel)

    def _load_feature(self, feature):
        props = feature['properties']
        is_way = props['klass'] == 'Section'
        osm_id = props['osm_id'] if 'osm_id' in props else None

        if osm_id and self.exclude_osm_elements:
            return

        id = osm_id or -props['id']

        self._extract_lines(id, is_way, props)
        tags = self._extract_feature_tags(is_way, props)
        metadata = self._extract_feature_metadata(props)

        if is_way:
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

    def _extract_feature_tags(self, is_way, props):
        tags = [('citylines:id', str(props['id']))]
        if 'osm_tags' in props:
            original_tags = json.loads(props['osm_tags'])
            for key in original_tags:
                tags.append((key, str(original_tags[key])))
        for line_info in props['lines']:
            if line_info['system']:
                tags.append(('network',line_info['system']))
        if not is_way:
            if not 'name' in dict(tags):
                tags.append(('name', props['name']))
            if not 'public_transport' in dict(tags):
                tags.append(('public_transport', 'stop_position'))
        return tags

    def _extract_feature_metadata(self, props):
        metadata = {'version': None}
        if 'osm_metadata' in props:
            metadata = json.loads(props['osm_metadata'])
        return metadata

    def _extract_lines(self, id, is_way, props):
        for line_info in props['lines']:
            name = line_info['line']
            if line_info['system']:
                name = line_info['system'] + ' ' + name
            if not name in self._relations_dict:
                self._relations_dict[name] = []
            t = 'w' if is_way else 'n'
            role = '' if is_way else 'stop'
            self._relations_dict[name].append({'id':id, 'type':t, 'role': role})
