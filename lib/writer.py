import osmium
from lib.parser import FeaturesParser
from lib.transport_modes import TransportModesProvider

class CitylinesWriter(object):
    def __init__(self, sections, stations, lines, output):
        self._features = sections + stations
        self.writer = osmium.SimpleWriter(output)
        self.transport_modes_provider = TransportModesProvider(lines)

    def run(self):
        parser = FeaturesParser(self._features, self.transport_modes_provider, exclude_osm_elements=True)
        parser.run()

        self.write_nodes(parser.nodes)
        self.write_ways(parser.ways)
        self.write_relations(parser.relations)
        self.writer.close()

    def write_nodes(self, nodes):
        for node in nodes:
            self.writer.add_node(node)

    def write_ways(self, ways):
        for way in ways:
            self.writer.add_way(way)

    def write_relations(self, relations):
        for relation in relations:
            self.writer.add_relation(relation)
