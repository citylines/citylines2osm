import osmium
import json

class Parser(object):
    def __init__(self, features):
        self.features = features
        self._nodes = []
        self._ways = []
        self._relations = []
        self._relations_dict = {}

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
        raise NotImplementedError

    def _member_type(self):
        raise NotImplementedError

    def _build_tags(self, props):
        tags = [('citylines:id', str(props['id']))]
        if 'osm_tags' in props:
            original_tags = json.loads(props['osm_tags'])
            for key in original_tags:
                tags.append((key, str(original_tags[key])))
        return tags

    def _extract_lines(self, id, props):
        for line_info in props['lines']:
            name = line_info['line']
            if line_info['system']:
                name = line_info['system'] + ' ' + name
            if not name in self._relations_dict:
                self._relations_dict[name] = []
            self._relations_dict[name].append(id)

    def load_relations(self):
        for i, rel_name in enumerate(self._relations_dict):
            rel = self._relations_dict[rel_name]
            tags = [('name',rel_name)]
            members = []
            for id in rel:
                members.append((self._member_type(), id,''))
            rel = osmium.osm.mutable.Relation(id=-(i+1),members=members,tags=tags)
            self._relations.append(rel)
