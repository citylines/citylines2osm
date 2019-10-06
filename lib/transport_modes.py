class TransportModesProvider(object):
    TRANSPORT_MODES = {
        '0': None,
        # High speed train
        '1': {
            'node': ('train','yes'),
            'way': ('railway','rail'),
            'relation': ('route','train')
            },
        # Intercity train
        '2': {
            'node': ('train','yes'),
            'way': ('railway','rail'),
            'relation': ('route','train')
            },
        # Commuter rail
        '3': {
            'node': ('train','yes'),
            'way': ('railway','rail'),
            'relation': ('route','train')
            },
        # Metro/Subway: default
        '4': {
            'node': ('subway','yes'),
            'way': ('railway','subway'),
            'relation': ('route','subway')
            },
        # Light rail
        '5': {
            'node':('light_rail','yes'),
            'way': ('railway','light_rail'),
            'relation': ('route','light_rail')
            },
        # BRT
        '6': {
            'node':('highway','bus_stop'),
            'way': ('busway','lane'),
            'relation': ('route','bus')
            },
        # People mover
        '7': None,
        # Bus
        '8': {
            'node':('highway','bus_stop'),
            'way': None,
            'relation': ('route','bus')
            },
        # Tram
        '9': {
            'node':('tram','yes'),
            'way': ('railway','tram'),
            'relation': ('route','tram')
            },
        # Ferry
        '10': {
            'node':[('ferry','yes'),('amenity','ferry_terminal')],
            'way': ('route','ferry'),
            'relation': ('route','ferry')
            }
        }

    def __init__(self, lines_info):
        self._lines = {}
        for line in lines_info:
            self._lines[line['url_name']] = line

    def tags(self, line_url_name, element_type):
        transport_mode_id = self._lines[line_url_name]['transport_mode_id']
        mode = self.TRANSPORT_MODES[str(transport_mode_id)] or self.TRANSPORT_MODES['4']
        tags = mode[element_type]
        if not isinstance(tags, list):
            tags = [tags]

        # We remove Nones from list
        tags = list(filter(None, tags))

        return tags
