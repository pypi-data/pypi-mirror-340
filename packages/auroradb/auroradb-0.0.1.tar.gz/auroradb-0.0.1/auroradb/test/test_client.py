from auroradb.src.client import AuroraDBClient
from unittest import TestCase

class AuroraDBClientTests(TestCase):
    DEFAULT_URL = "mongodb://localhost:27017/"
    DEFAULT_DB = "portfoliodb"
    DEFAULT_TBL = 'instruments'
    DEFAULT_INST = 'SPX.CALL.1'

    def setUp(self):
        self.client = AuroraDBClient(self.DEFAULT_URL, self.DEFAULT_DB, self.DEFAULT_TBL)

    def test_Construction(self):
        self.assertIsNotNone(self.client.connection)

    def test_getitem(self):
        key, value = 'Instrument', self.DEFAULT_INST
        identifier = (key, value)
        data = self.client[identifier]
        self.assertIsNotNone(data)
        self.assertEquals(value, data[key])