import json

class Parser(object):
    def __init__(self, features):
        self.features = features
        self._nodes = []
        self._ways = []
        self._relations = []

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

    def _tags(self, props):
        tags = [('citylines:id', str(props['id']))]
        if 'osm_tags' in props:
            original_tags = json.loads(props['osm_tags'])
            for key in original_tags:
                tags.append((key, str(original_tags[key])))
        return tags
