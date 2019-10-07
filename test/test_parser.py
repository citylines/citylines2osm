import unittest
from lib.parser import FeaturesParser
from lib.transport_modes import TransportModesProvider

class TestFeaturesParser(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.section = {
            'properties': {
                'id': 1,
                'klass': 'Section',
                'lines': [{'system': 'Metro', 'line': 'L1', 'line_url_name':'l1'}]
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
                'lines': [{'system': 'Metro', 'line': 'L1', 'line_url_name':'l1'}]
            },
            'geometry': {
                'coordinates': [[11,22]]
            }
        }

        self.osm_section = {
            'properties': {
                'id': 1,
                'klass': 'Section',
                'lines': [{'system': 'Metro', 'line': 'L1', 'line_url_name':'l1'}],
                'osm_id':'44441',
                'osm_tags': '{"previous":"tag"}',
                'osm_metadata': '{"version":2}'
            },
            'geometry': {
                'coordinates': [[10,20],[12,24]]
            }
        }

        self.osm_station = {
            'properties': {
                'id': 3,
                'klass': 'Station',
                'name': 'Clot',
                'lines': [{'system': 'Metro', 'line': 'L1', 'line_url_name':'l1'}],
                'osm_id':'33331',
                'osm_tags': '{"previous":"tag"}',
                'osm_metadata':'{"version":3}'
            },
            'geometry': {
                'coordinates': [[11,22]]
            }
        }

        lines_info = [ {'url_name':'l1', 'transport_mode_id':4,'transport_mode_name': 'heavy_rail'}]
        self.transport_modes_provider = TransportModesProvider(lines_info)

    def test_non_osm_features(self):
        parser = FeaturesParser([self.section, self.station], self.transport_modes_provider)
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

                expected_tags = [('citylines:id',str(station_id)),('network', 'Metro'),('railway','station'),('subway','yes'),('name','Clot'),('public_transport','stop_position')]
                self.assertEqual(expected_tags, node.tags)

        # Ways
        # ====
        way = parser.ways[0]
        self.assertEqual(-section_id, way.id)

        expected_tags = [('citylines:id', str(section_id)), ('network', 'Metro'),('railway','subway'),('tunnel','yes')]
        self.assertEqual(expected_tags, way.tags)

        self.assertEqual([-1, -2], way.nodes)

        # Relations
        # =========
        relation = parser.relations[0]
        self.assertEqual(-1, relation.id)

        expected_tags = [('name', 'Metro L1'),('type', 'route'),('public_transport:version','2'),('route','subway')]
        self.assertEqual(expected_tags, relation.tags)

        expected_members = [('w',-section_id, ''),('n', -station_id, 'stop')]
        self.assertEqual(expected_members, relation.members)

    def test_osm_features(self):
        parser = FeaturesParser([self.osm_section, self.osm_station], self.transport_modes_provider)
        parser.run()

        station_id = self.station['properties']['id']
        section_id = self.section['properties']['id']
        station_osm_id = self.osm_station['properties']['osm_id']
        section_osm_id = self.osm_section['properties']['osm_id']

        # Nodes
        # =====
        # As no refs are set by default in osm ways (because citylines doesn't store it),
        # only the station node is available
        node = parser.nodes[0]
        self.assertEqual(self.osm_station['geometry']['coordinates'], node.location)
        self.assertEqual(station_osm_id, node.id)
        self.assertEqual(3, node.version)

        expected_tags = [('citylines:id',str(station_id)),('previous','tag'),('network', 'Metro'),('railway','station'),('subway','yes'),('name','Clot'),('public_transport','stop_position')]
        self.assertEqual(expected_tags, node.tags)

        # Ways
        # ====
        way = parser.ways[0]
        self.assertEqual(section_osm_id, way.id)
        self.assertEqual(2, way.version)

        expected_tags = [('citylines:id', str(section_id)),('previous','tag'),('network', 'Metro'),('railway','subway'),('tunnel','yes')]
        self.assertEqual(expected_tags, way.tags)

        # Relations
        # =========
        relation = parser.relations[0]
        self.assertEqual(-1, relation.id)

        expected_tags = [('name', 'Metro L1'),('type', 'route'),('public_transport:version','2'),('route','subway')]
        self.assertEqual(expected_tags, relation.tags)

        expected_members = [('w',section_osm_id, ''),('n', station_osm_id, 'stop')]
        self.assertEqual(expected_members, relation.members)
