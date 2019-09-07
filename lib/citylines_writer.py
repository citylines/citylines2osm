import osmium
from lib.sections_parser import SectionsParser
from lib.stations_parser import StationsParser

class CitylinesWriter(object):
    def __init__(self, sections, stations, output):
        self._sections = sections
        self._stations = stations
        self.writer = osmium.SimpleWriter(output)

    def call(self):
        stations_parser = StationsParser(self._stations)
        stations_parser.run()
        sections_parser = SectionsParser(self._sections)
        sections_parser.run()

        self.write_nodes(stations_parser.nodes)

        self.write_nodes(sections_parser.nodes)
        self.write_ways(sections_parser.ways)
        self.write_relations(sections_parser.relations)
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
