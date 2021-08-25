import json
import pytest
import sys
from unittest import TestCase
from events_processor import app


class TestAppFile(TestCase):
    def setUp(self) -> None:
        sys.path.insert(0, "../../mindsphere_time_series")
        return

    def test_lambda_handler(self):
        with open('./events/test_kinesis_event.json') as json_file:
            event = json.load(json_file)
            result = app.lambda_handler(event, {})
            self.assertTrue(result != None)
            self.assertTrue(result["statusCode"] == 200)
