# Lambda handler tests (mocked S3).

import importlib.util
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Set env and mock boto3 before app loads
with patch.dict("os.environ", {"RAW_BUCKET": "test-raw-bucket"}):
    mock_boto3 = MagicMock()
    sys.modules["boto3"] = mock_boto3

    app_path = Path(__file__).resolve().parent.parent / "ingestion" / "lambda" / "app.py"
    spec = importlib.util.spec_from_file_location("app", app_path)
    app_mod = importlib.util.module_from_spec(spec)
    sys.modules["app"] = app_mod
    spec.loader.exec_module(app_mod)


class TestLambdaHandler(unittest.TestCase):
    def test_lambda_handler_with_load_date(self):
        mock_s3 = MagicMock()
        mock_boto3.client.return_value = mock_s3

        with patch("app.os.path.exists", return_value=True), patch("app.os.path.getsize", return_value=100):
            event = {"load_date": "2024-03-14"}
            result = app_mod.lambda_handler(event, None)

        self.assertEqual(result["statusCode"], 200)
        body = json.loads(result["body"])
        self.assertIn("uploaded_count", body)
        self.assertEqual(body["load_date"], "2024-03-14")
        self.assertIn("uploaded", body)

    def test_lambda_handler_returns_uploaded_count(self):
        mock_s3 = MagicMock()
        mock_boto3.client.return_value = mock_s3

        with patch("app.os.path.exists", return_value=True), patch("app.os.path.getsize", return_value=50):
            event = {}
            result = app_mod.lambda_handler(event, None)

        self.assertEqual(result["statusCode"], 200)
        body = json.loads(result["body"])
        self.assertIn("uploaded_count", body)
        self.assertIsInstance(body["uploaded_count"], int)


if __name__ == "__main__":
    unittest.main()
