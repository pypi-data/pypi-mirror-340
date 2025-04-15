import unittest

from auroradb.api.api import connect, save, load
from unittest import TestCase

class AuroraDBApiTests(TestCase):
    DEFAULT_URL = "mongodb://localhost:27017/"
    BAD_URL = "mongodb://localhost:55555/"
    DEFAULT_DB = "portfoliodb"
    DEFAULT_TBL = 'instruments'
    DEFAULT_INST = 'SPX.CALL.1'

    def test_connectSuccess(self):
        client = connect(self.DEFAULT_URL, self.DEFAULT_DB, self.DEFAULT_TBL)
        self.assertIsNotNone(client)

    @unittest.skip
    def test_connectFailure(self):
        client = connect(self.BAD_URL, self.DEFAULT_DB, self.DEFAULT_TBL)
        self.assertIsNone(client)

    def test_loadSucess(self):
        client = connect(self.DEFAULT_URL, self.DEFAULT_DB, self.DEFAULT_TBL)
        key, value = 'Instrument', self.DEFAULT_INST
        data = client[{key : value}]
        self.assertIsNotNone(data)
        self.assertEquals(value, data[key])