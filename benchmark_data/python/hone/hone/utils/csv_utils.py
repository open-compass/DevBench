"""
Simple helper methods for processing CSV files
"""

from contextlib import contextmanager
import csv
import fileinput

class CSVUtils:
    def __init__(self, csv_filepath):
        self.filepath = csv_filepath

    # Parses and returns first row of CSV (column names)
    def get_column_names(self):
        with self.open_csv() as f:
            csvreader = csv.reader(f)
            cols = next(csvreader)
        return cols

    # Returns parsed rows of CSV (excluding column names)
    def get_data_rows(self):
        with self.open_csv() as f:
            csvreader = csv.reader(f)
            parsed_csv = list(csvreader)
            data_rows = parsed_csv[1:]  # discard column names
        return data_rows

    # Open CSV in given mode (default is read mode)
    @contextmanager
    def open_csv(self, mode='r', newline=''):
        f = fileinput.input(files=(self.filepath), openhook=fileinput.hook_encoded("utf-8-sig"))
        try:
            yield f
        finally:
            f.close()
