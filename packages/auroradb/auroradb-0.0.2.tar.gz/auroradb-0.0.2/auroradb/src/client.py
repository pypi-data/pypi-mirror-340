import pymongo

class AuroraDBClient:

    def __init__(self, url : str, database : str, table : str):
        self._url = url
        self._connection = self._connect()
        self._database = database
        self._table = table

    def _connect(self):
        return pymongo.MongoClient(self._url, connect=True)

    @property
    def connection(self):
        return self._connection

    def __getitem__(self, locator):
        return self._connection[self._database][self._table].find_one(locator)