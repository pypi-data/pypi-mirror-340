from auroradb.api.api import connect, save, load
from unittest import TestCase

class AuroraDBApiTests(TestCase):
    #DEFAULT_URL = "mongodb://localhost:27017/"
    DEFAULT_URL = "mongodb://localhost:27990/"
    DEFAULT_DB = "portfoliodb"
    DEFAULT_TBL = 'instruments'
    DEFAULT_INST = 'SPX.CALL.1'

    def test_connect(self):
        client = connect(self.DEFAULT_URL, self.DEFAULT_DB, self.DEFAULT_TBL)
        self.assertIsNotNone(client)

    def test_load(self):
        client = connect(self.DEFAULT_URL, self.DEFAULT_DB, self.DEFAULT_TBL)
        key, value = 'Instrument', self.DEFAULT_INST
        data = client[(key, value)]
        self.assertIsNotNone(data)
        self.assertEquals(value, data[key])