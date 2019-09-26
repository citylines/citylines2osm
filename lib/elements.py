import osmium
import json

class Element(object):
    def __init__(self, feature):
        self._props = feature['properties']
        self._geometry = feature['geometry']
        self.osm_id = self._props['osm_id'] if 'osm_id' in self._props else None
        self.id = self.osm_id or -self._props['id']
        self._tags  = self._build_tags()
        self._metadata = self._build_metadata()

    def member_type(self):
        raise NotImplementedError

    def member_role(self):
        raise NotImplementedError

    def _build_tags(self):
        props = self._props
        tags = [('citylines:id', str(props['id']))]
        if 'osm_tags' in props:
            original_tags = json.loads(props['osm_tags'])
            for key in original_tags:
                tags.append((key, str(original_tags[key])))

        for line_info in props['lines']:
            if line_info['system']:
                tags.append(('network',line_info['system']))

        transport_mode_tags = self._transport_mode_tags()
        if transport_mode_tags:
            tags.append(transport_mode_tags)

        return tags

    def _transport_mode_tags(self):
        # TODO: WAY:  set for example railway=subway
        # TODO: NODE: set for example subway=yes
        # TODO: RELATION: set for example route=subway
        return None

    def _build_metadata(self):
        metadata = {'version': None}
        if 'osm_metadata' in self._props:
            metadata = json.loads(self._props['osm_metadata'])
        return metadata

    def lines_info(self):
        lines = []
        for line_info in self._props['lines']:
            name = line_info['line']
            if line_info['system']:
                name = line_info['system'] + ' ' + name
            transport_mode = None # TODO
            lines.append({'name': name, 'transport_mode': transport_mode})
        return lines

    def osmium_object(self):
        raise NotImplementedError

class Way(Element):
    def __init__(self, feature, nodes_count):
        super().__init__(feature)
        self._nodes_count = nodes_count
        self._nodes = []
        self._refs = [] if self.osm_id else self._load_nodes()

    def member_type(self):
        return 'w'

    def member_role(self):
        return ''

    def _load_nodes(self):
        refs = []
        for lonlat in self._geometry['coordinates']:
            id = -(self._nodes_count + len(self._nodes) + 1)
            refs.append(id)
            self._nodes.append(osmium.osm.mutable.Node(id=id, location=lonlat))
        return refs

    def nodes(self):
        return self._nodes

    def osmium_object(self):
        return osmium.osm.mutable.Way(id=self.id, nodes=self._refs, tags=self._tags, version=self._metadata['version'])


class Node(Element):
    def member_type(self):
        return 'n'

    def member_role(self):
        return 'stop'

    def _build_tags(self):
        tags = super()._build_tags()

        if not 'name' in dict(tags):
            tags.append(('name', self._props['name']))
        if not 'public_transport' in dict(tags):
            tags.append(('public_transport', 'stop_position'))

        return tags

    def osmium_object(self):
        lonlat = self._geometry['coordinates']
        return osmium.osm.mutable.Node(id=self.id, location=lonlat, tags=self._tags, version=self._metadata['version'])
