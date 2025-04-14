from auroradb.src.client import AuroraDBClient

def connect(url : str, db : str, table : str):
    if not any([url, db, table]):
        raise RuntimeError(f'Missing arguments : URL={url}, DataBase={db}, Collection={table}')
    try:
        client = AuroraDBClient(url, db, table)
    except Exception as exp:
        print(f'Error in connecting to auroradb at {url}')
    return client

def save(client, data):
    pass

def load(client, key, value):
    return client[(key, value)]