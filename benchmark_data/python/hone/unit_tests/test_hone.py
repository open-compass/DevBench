import os
import unittest
from hone import hone
from hone.utils import test_utils

dirname = os.path.dirname(os.path.dirname(__file__))
csv_A_path = os.path.join(dirname, "data_file", "small_cats_dataset", "dataset.csv")
json_A_path = os.path.join(dirname, "data_file", "small_cats_dataset", "nested_dataset.json")
json_schema_A_path = os.path.join(dirname, "data_file", "small_cats_dataset", "nested_schema.json")
csv_B_path = os.path.join(dirname, "data_file", "comma_test", "dataset.csv")
json_B_path = os.path.join(dirname, "data_file", "comma_test", "nested_dataset.json")
csv_C_path = os.path.join(dirname, "data_file", "quotes_test", "dataset.csv")
json_C_path = os.path.join(dirname, "data_file", "quotes_test", "nested_dataset.json")

class TestHone(unittest.TestCase):
    def test_nest_small_csv(self):
        h = hone.Hone()
        actual_result = h.convert(csv_A_path)
        expected_result = test_utils.parse_json_file(json_A_path)
        self.assertListEqual(actual_result, expected_result)
    def test_get_schema(self):
        h = hone.Hone()
        actual_schema = h.get_schema(csv_A_path)
        expected_schema = test_utils.parse_json_file(json_schema_A_path)
        self.assertDictEqual(actual_schema, expected_schema)
        actual_result = h.convert(csv_A_path, actual_schema)
        expected_result = test_utils.parse_json_file(json_A_path)
        self.assertListEqual(actual_result, expected_result)
    def test_nest_comma_csv(self):
        h = hone.Hone()
        actual_result = h.convert(csv_B_path)
        expected_result = test_utils.parse_json_file(json_B_path)
        self.assertListEqual(actual_result, expected_result)
    def test_nest_quotes_csv(self):
        h = hone.Hone()
        actual_result = h.convert(csv_C_path)
        expected_result = test_utils.parse_json_file(json_C_path)
        self.assertListEqual(actual_result, expected_result)


if __name__ == '__main__':
    unittest.main()
