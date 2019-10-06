import osmium
import json

class Element(object):
    def __init__(self, feature, transport_modes_provider):
        self._props = feature['properties']
        self._geometry = feature['geometry']
        self.osm_id = self._props['osm_id'] if 'osm_id' in self._props else None
        self.id = self.osm_id or -self._props['id']
        self._transport_modes_provider = transport_modes_provider
        self._tags  = self._build_tags()
        self._metadata = self._build_metadata()

    def member(self):
        # (type, id, role)
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

        tags += self._transport_mode_tags()

        return tags

    def _transport_mode_tags(self):
        line_url_name = self.lines_info()[0]['url_name']
        return self._transport_modes_provider.tags(line_url_name, self.__class__.__name__.lower())

    def _build_metadata(self):
        metadata = {'version': None}
        if 'osm_metadata' in self._props:
            metadata = json.loads(self._props['osm_metadata'])
        return metadata

    def lines_info(self):
        lines = []
        for line in self._props['lines']:
            name = line['line']
            if line['system']:
                name = line['system'] + ' ' + name
            lines.append({'name': name, 'url_name': line['line_url_name']})
        return lines

    def osmium_object(self):
        raise NotImplementedError

class Way(Element):
    def __init__(self, feature, transport_modes_provider, nodes_count):
        super().__init__(feature, transport_modes_provider)
        self._nodes_count = nodes_count
        self._nodes = []
        self._refs = [] if self.osm_id else self._load_nodes()

    def member(self):
        return ('w', self.id, '')

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
    def member(self):
        return ('n', self.id, 'stop')

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

class Relation(Element):
    def __init__(self, transport_modes_provider, args):
        self.id = args['id']
        self._name = args['name']
        self._members = args['members']

        # We mock the lines info so the line_url_name can be fetch through #lines_info
        self._props = {'lines': [{'line':'', 'system':None, 'line_url_name':args['url_name']}]}

        self._transport_modes_provider = transport_modes_provider
        self._tags = self._build_tags()

    def _build_tags(self):
        tags = [('name',self._name),('type','route'),('public_transport:version','2')]
        tags += self._transport_mode_tags()
        return tags

    def osmium_object(self):
        return osmium.osm.mutable.Relation(id=self.id,members=self._members,tags=self._tags)
