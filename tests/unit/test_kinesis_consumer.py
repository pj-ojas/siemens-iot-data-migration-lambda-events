import json

import pytest
import pytest
from unittest import TestCase
from events_processor import app
from events_processor.kinesis_consumer import KinesisConsumer
from tests.unit.kinesis_test_api import KinesisTestApi


class TestKinesisConsumer(TestCase):
    def test_kinesis_consumer(self):
        kinesis_consumer = KinesisConsumer()
        self.assertTrue(kinesis_consumer.subscribe())

    def test_get_record(self):
        api = KinesisTestApi()
        api.put_record('some data new 123')
