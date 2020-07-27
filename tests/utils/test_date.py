import unittest
from stronk.utils import date as date_util

class TestDateUtils(unittest.TestCase):
    def test_date_str_to_date(self):
        test_date = "2020-01-20"
        date = date_util.date_str_to_date(test_date)
        self.assertEqual(date.year, 2020, "year")
        self.assertEqual(date.month, 1, "month")
        self.assertEqual(date.day, 20, "day")

    def test_date_time_str_to_date(self):
        test_date_time = "2020-01-20T12:03:40+00:00"
        date = date_util.date_time_str_to_date(test_date_time)
        self.assertEqual(date.year, 2020, "year")
        self.assertEqual(date.month, 1, "month")
        self.assertEqual(date.day, 20, "day")
        self.assertEqual(date.timetz().hour, 12, "hour")
        self.assertEqual(date.timetz().minute, 3, "minute")
        self.assertEqual(date.timetz().second, 40, "secong")
        self.assertEqual(date.timetz().tzname(), "UTC")

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)