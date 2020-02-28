import datetime
import os
import unittest
from unittest import mock

import app_mealservice_records as records
from backup import csv_service


class CSVServiceTestCase(unittest.TestCase):
    def setUp(self):
        """Setup datetime mock"""
        datetime_patcher = mock.patch("backup.csv_service.datetime")
        mocked_datetime = datetime_patcher.start()
        mocked_datetime.now.return_value = datetime.datetime(2002, 3, 1)
        self.addCleanup(datetime_patcher.stop)

    def test_generate_file_name(self):
        filename = csv_service.generate_file_name()
        self.assertEqual(filename, "backup_FEB_2002")

    def test_create_csv(self):
        csv_path, filename = csv_service.create_csv(records.records)
        self.assertEqual(csv_path, f"backup/csvs/{filename}.csv")
        # clean up
        os.remove("backup/csvs/backup_FEB_2002.csv")


if __name__ == "__main__":
    unittest.main()
