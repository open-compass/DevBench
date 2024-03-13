import unittest
from datetime import datetime
from query_arxiv import check_date

class TestCheckDate(unittest.TestCase):

    def test_within_range(self):
        """
        Test case where the submission date is within the range of recent_days from the current date.
        """
        date_string = "2023-01-01T00:00:00Z"
        recent_days = 10
        current_date = datetime(2023, 1, 11)  # This makes it exactly 10 days from the submission date
        result = check_date(date_string, recent_days, current_date)
        self.assertTrue(result)

    def test_out_of_range(self):
        """
        Test case where the submission date is outside the range of recent_days from the current date.
        """
        date_string = "2023-01-01T00:00:00Z"
        recent_days = 10
        current_date = datetime(2023, 1, 15)  # This makes it 14 days from the submission date, which is out of the range considering DATE_OFFSET
        result = check_date(date_string, recent_days, current_date)
        self.assertFalse(result)

    def test_invalid_date_format(self):
        """
        Test case where the date_string is not in the expected format. This should raise a ValueError.
        """
        date_string = "Invalid-Date-Format"
        recent_days = 10
        current_date = datetime.now()

        with self.assertRaises(ValueError):
            check_date(date_string, recent_days, current_date)

if __name__ == "__main__":
    unittest.main()
