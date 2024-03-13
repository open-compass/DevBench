# acceptance_tests/test_acceptance.py

import unittest
import os
from collections import OrderedDict

from geotext.geotext import GeoText

class TestGeoTextAcceptance(unittest.TestCase):

    def setUp(self):
        self.data_path = os.path.join(os.path.dirname(__file__), '..', 'geotext', 'data_file')

    def test_city_extraction(self):
        text = "London is a great city"
        places = GeoText(text)
        self.assertIn('London', places.cities)

    def test_country_mentions_count(self):
        text = 'New York, Texas, and also China'
        places = GeoText(text)
        expected = OrderedDict([(u'US', 2), (u'CN', 1)])
        self.assertEqual(places.country_mentions, expected)

    def test_country_filter(self):
        text = 'I loved Rio de Janeiro and Havana'
        places = GeoText(text, 'BR')
        self.assertIn('Rio de Janeiro', places.cities)
        self.assertNotIn('Havana', places.cities)

    def test_nationalities_extraction(self):
        text = "German engineers are known for their precision."
        places = GeoText(text)
        self.assertIn('German', places.nationalities)

    def test_data_loading(self):
        places = GeoText('')
        self.assertTrue(hasattr(places.index, 'cities'))
        self.assertTrue(hasattr(places.index, 'countries'))
        self.assertTrue(hasattr(places.index, 'nationalities'))


if __name__ == '__main__':
    unittest.main()
