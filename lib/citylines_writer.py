import osmium
from lib.sections_parser import SectionsParser

class CitylinesWriter(object):
    def __init__(self, sections, output):
        self.sections = sections
        self.writer = osmium.SimpleWriter(output)

    def call(self):
        sections_parser = SectionsParser(self.sections)
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
