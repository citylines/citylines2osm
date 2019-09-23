import unittest
import osmium
from lib.parser import FeaturesParser

class TestFeaturesParser(unittest.TestCase):
    SECTION_TAGS = ['citylines:id', 'network']
    STATION_TAGS = SECTION_TAGS + ['name', 'public_transport']
    LINE_TAGS = ['name', 'type']

    @classmethod
    def setUpClass(self):
        self.section = {
            'properties': {
                'id': 1,
                'klass': 'Section',
                'lines': [{'system': 'Metro', 'line': 'L1'}]
            },
            'geometry': {
                'coordinates': [[10,20],[12,24]]
            }
        }

        self.station = {
            'properties': {
                'id': 3,
                'klass': 'Station',
                'name': 'Clot',
                'lines': [{'system': 'Metro', 'line': 'L1'}]
            },
            'geometry': {
                'coordinates': [[11,22]]
            }
        }

    def test_non_osm_features(self):
        parser = FeaturesParser(features=[self.section, self.station])
        parser.run()

        # Nodes
        # =====
        for i, node in enumerate(parser.nodes):
            self.assertEqual(osmium.osm.mutable.Node, node.__class__)

            # the two first nodes belong to the sections'way
            if i < 2:
                self.assertEqual(self.section['geometry']['coordinates'][i], node.location)
                self.assertEqual(-(i+1), node.id)
            # the third one belongs to the station
            else:
                self.assertEqual(self.station['geometry']['coordinates'], node.location)
                self.assertEqual(-self.station['properties']['id'], node.id)

                # station tags
                for i, tag in enumerate(node.tags):
                    self.assertEqual(self.STATION_TAGS[i], tag[0])

        # Ways
        # ====
        way = parser.ways[0]
        self.assertEqual(osmium.osm.mutable.Way, way.__class__)
        self.assertEqual(-self.section['properties']['id'], way.id)

        # section tags
        for i, tag in enumerate(way.tags):
            self.assertEqual(self.SECTION_TAGS[i], tag[0])

        # refs
        refs = [-1, -2]
        for i, ref in enumerate(way.nodes):
            self.assertEqual(refs[i], ref)

        # Relations
        # =========
        relation = parser.relations[0]
        self.assertEqual(osmium.osm.mutable.Relation, relation.__class__)
        self.assertEqual(-1, relation.id)

        # relation tags
        for i, tag in enumerate(relation.tags):
            self.assertEqual(self.LINE_TAGS[i], tag[0])

        # members
        expected_members = [
                ('w',-self.section['properties']['id'], ''),
                ('n', -self.station['properties']['id'],'')
                ]
        self.assertEqual(expected_members, relation.members)
