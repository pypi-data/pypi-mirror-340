import pymongo
from datetime import date
import bson

class Instrument:
    def __init__(self, iid):
        self._iid = iid

class VanillaOption(Instrument):
    def __init__(self, iid, asset : str, creationDate : date, maturityDate : date, kind : str, strike : float):
        super().__init__(iid)
        self._asset = asset
        self._creationDate = creationDate
        self._maturityDate = maturityDate
        self._kind = kind
        self._strike = strike

    def encode(self):
        params = {'Asset' : self._asset,
                  'Creation' : self._creationDate.strftime('%Y-%m-%d'),
                  'Maturity' : self._maturityDate.strftime('%Y-%m-%d'),
                  'Kind' : self._kind,
                  'Strike' : self._strike}
        encodedParams = bson.encode(params)
        doc = {'Instrument' : self._iid, 'Type' : 'VanillaOption', 'Attributes' : encodedParams}
        return doc

    def save(self, conn):
        encoded = self.encode()
        db = conn["portfoliodb"]
        coll = db["instruments"]
        coll.insert_one(encoded)

    @staticmethod
    def load(instId, conn):
        db = conn["portfoliodb"]
        coll = db["instruments"]
        inst = coll.find_one()

vCall = VanillaOption(iid = 'SPX.CALL.1', asset = 'SPX', creationDate = date(2025, 1, 1), maturityDate = date(2025, 12, 31), kind = 'C', strike = 110.0)
vCallEnc = vCall.encode()

vPut = VanillaOption(iid = 'SPX.PUT.1', asset = 'SPX', creationDate = date(2025, 1, 1), maturityDate = date(2025, 12, 31), kind = 'P', strike = 90.0)
vPutEnc = vPut.encode()

print(f'Call : {vCallEnc}')
print(f'Put : {vPutEnc}')

'''
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
a = mycol.insert_one(vCallEnc)
b = mycol.insert_one(vPutEnc)
'''
