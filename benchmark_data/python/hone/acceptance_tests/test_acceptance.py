import unittest
import json
import os
from hone.hone import Hone


class CSVtoJSONAcceptanceTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # The base directory is the 'hone' directory
        cls.base_directory = os.path.dirname(os.path.dirname(__file__))
        cls.hone = Hone()

    def compare_json_output(self, csv_relative_path, json_relative_path):
        csv_path = os.path.join(self.base_directory, csv_relative_path)
        json_path = os.path.join(self.base_directory, json_relative_path)

        # Convert CSV to JSON
        actual_json_struct = self.hone.convert(csv_path)
        
        # Read the expected JSON structure
        with open(json_path, 'r') as f:
            expected_json_struct = json.load(f)
        
        # Assert that the actual JSON matches the expected JSON
        self.assertEqual(actual_json_struct, expected_json_struct)

    def test_comma_handling(self):
        self.compare_json_output('data_file/comma_test/dataset.csv', 
                                 'data_file/comma_test/nested_dataset.json')

    def test_quoted_field_handling(self):
        self.compare_json_output('data_file/quotes_test/dataset.csv', 
                                 'data_file/quotes_test/nested_dataset.json')

    def test_nested_json_generation(self):
        schema_path = os.path.join(self.base_directory, 'data_file/small_cats_dataset/nested_schema.json')
        with open(schema_path, 'r') as schema_file:
            schema = json.load(schema_file)
        self.compare_json_output('data_file/small_cats_dataset/dataset.csv', 
                                 'data_file/small_cats_dataset/nested_dataset.json')

    def test_data_integrity(self):
        self.compare_json_output('data_file/small_cats_dataset/dataset.csv', 
                                 'data_file/small_cats_dataset/nested_dataset.json')

    def test_error_handling(self):
        with self.assertRaises(Exception):
            self.hone.convert(os.path.join(self.base_directory, 'data_file/nonexistent.csv'))

if __name__ == '__main__':
    unittest.main()
