import datetime
import os
import unittest
from unittest import mock

import app_mealservice_records as records
from backup import csv_service, gdrive


class GDriveTestCase(unittest.TestCase):
    def setUp(self):
        datetime_patcher = mock.patch("backup.csv_service.datetime")
        mocked_datetime = datetime_patcher.start()
        mocked_datetime.now.return_value = datetime.datetime(2002, 4, 1)
        self.csv_path, self.filename = csv_service.create_csv(records.records)
        self.addCleanup(datetime_patcher.stop)
        self.addCleanup(lambda file_path: os.remove(file_path), self.csv_path)

    @mock.patch("requests.post")
    def test_upload_to_drive(self, mock_post):
        mock_post.return_value = mock.Mock(ok=True)
        mock_post.return_value.json.return_value = {"name": f"{self.filename}"}

        resp_body = gdrive.upload_to_drive(self.csv_path, self.filename)

        self.assertIsInstance(resp_body, dict)
        self.assertEqual(resp_body["name"], self.filename)


if __name__ == "__main__":
    unittest.main()
