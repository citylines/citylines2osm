class TransportMode(object):
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
        # Metro/Subway
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

    def __init__(self, transport_mode_id, element_type):
        self._transport_mode_id = transport_mode_id
        self._element_type = element_type

    def tags(self):
        mode = self.TRANSPORT_MODES[str(self._transport_mode_id)] or self.TRANSPORT_MODES['4']
        tags = mode[self._element_type]
        if not isinstance(tags, list):
            tags = list(tags)
        return tags
