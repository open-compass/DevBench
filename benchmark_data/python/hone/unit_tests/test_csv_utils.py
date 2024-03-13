import os
import unittest
import json
from hone.hone import Hone

# Setting up paths for test files
dirname = os.path.dirname(os.path.dirname(__file__))
test_directories = ["small_cats_dataset", "comma_test", "quotes_test"]
csv_paths = [os.path.join(dirname, "data_file", directory, "dataset.csv") for directory in test_directories]
json_paths = [os.path.join(dirname, "data_file", directory, "nested_dataset.json") for directory in test_directories]
schema_path = os.path.join(dirname, "data_file", "small_cats_dataset", "nested_schema.json")

class AcceptanceTestCSVtoJSON(unittest.TestCase):

    def test_full_conversion_small_cats_dataset(self):
        """Test conversion for small cats dataset with provided schema."""
        hone_instance = Hone()
        with open(schema_path, 'r') as schema_file:
            schema = json.load(schema_file)
        actual_result = hone_instance.convert(csv_paths[0], schema=schema)
        with open(json_paths[0], 'r') as json_file:
            expected_result = json.load(json_file)
        self.assertEqual(actual_result, expected_result, "The conversion for the small cats dataset did not match the expected output.")
    
    def test_full_conversion_comma_test(self):
        """Test conversion for dataset with complex comma usage."""
        hone_instance = Hone()
        actual_result = hone_instance.convert(csv_paths[1])
        with open(json_paths[1], 'r') as json_file:
            expected_result = json.load(json_file)
        self.assertEqual(actual_result, expected_result, "The conversion for the comma test did not match the expected output.")
    
    def test_full_conversion_quotes_test(self):
        """Test conversion for dataset with complex quoting."""
        hone_instance = Hone()
        actual_result = hone_instance.convert(csv_paths[2])
        with open(json_paths[2], 'r') as json_file:
            expected_result = json.load(json_file)
        self.assertEqual(actual_result, expected_result, "The conversion for the quotes test did not match the expected output.")

if __name__ == '__main__':
    unittest.main()
