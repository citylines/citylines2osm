import unittest
import osmium
from lib.parser import FeaturesParser

class TestFeaturesParser(unittest.TestCase):
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

        station_id = self.station['properties']['id']
        section_id = self.section['properties']['id']

        # Nodes
        # =====
        for i, node in enumerate(parser.nodes):
            # the two first nodes belong to the sections'way
            if i < 2:
                self.assertEqual(self.section['geometry']['coordinates'][i], node.location)
                self.assertEqual(-(i+1), node.id)
            # the third one belongs to the station
            else:
                self.assertEqual(self.station['geometry']['coordinates'], node.location)
                self.assertEqual(-station_id, node.id)

                expected_tags = [('citylines:id',str(station_id)),('network', 'Metro'),('name','Clot'),('public_transport','stop')]
                self.assertEqual(expected_tags, node.tags)

        # Ways
        # ====
        way = parser.ways[0]
        self.assertEqual(-section_id, way.id)

        expected_tags = [('citylines:id', str(section_id)), ('network', 'Metro')]
        self.assertEqual(expected_tags, way.tags)

        self.assertEqual([-1, -2], way.nodes)

        # Relations
        # =========
        relation = parser.relations[0]
        self.assertEqual(-1, relation.id)

        expected_tags = [('name', 'Metro L1'),('type', 'route')]
        self.assertEqual(expected_tags, relation.tags)

        expected_members = [('w',-section_id, ''),('n', -station_id,'')]
        self.assertEqual(expected_members, relation.members)
