# Script to test the Analytics class.

from analytics import Analytics
import unittest
from datetime import datetime


class TestAnalytics(unittest.TestCase):

    def test_0_day_window(self):
        """Test the class when refund window is zero days."""

        test_date = datetime.strptime('2020-05-30', "%Y-%m-%d")
        analysis = Analytics(filename='transactions_sample.csv', datetime_now=test_date, refund_window=0)

        for index, row in analysis.monthly.iterrows():
            if row['Year Month'] == '2020-04':
                self.assertEqual(row['Sales'], 50 + 50)
                self.assertEqual(row['Refunds'], 50)
                self.assertEqual(row['Refund Rate'], 50 / (50 + 50))
            elif row['Year Month'] == '2020-05':
                self.assertEqual(row['Sales'], 100 + 200)
                self.assertEqual(row['Refunds'], 100 + 50)
                self.assertEqual(row['Refund Rate'], (100 + 50) / (100 + 200))

    def test_14_day_window(self):
        """Test the class when refund window is 14 days."""

        test_date = datetime.strptime('2020-05-30', "%Y-%m-%d")
        analysis = Analytics(filename='transactions_sample.csv', datetime_now=test_date, refund_window=14)

        for index, row in analysis.monthly.iterrows():
            if row['Year Month'] == '2020-04':
                self.assertEqual(row['Sales'], 50 + 50)
                self.assertEqual(row['Refunds'], 50)
                self.assertEqual(row['Refund Rate'], 50 / (50 + 50))
            elif row['Year Month'] == '2020-05':
                self.assertEqual(row['Sales'], 200)
                self.assertEqual(row['Refunds'], 50)
                self.assertEqual(row['Refund Rate'], 50 / 200)


if __name__ == '__main__':
    unittest.main()
