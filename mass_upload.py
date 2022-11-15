import pymongo
import pandas as pd
import os
from io import BytesIO


df: pd.DataFrame = pd.read_excel('WinRates.xlsx')
records: list= df.to_dict('records')

for i, x in enumerate(records):
    print(x)
    records[i] = {
        '_id': x['ID'],
        'winningMC': x['winningMC'],
        'losingMC': x['losingMC'],
        'winningplayer': x['winningplayer'],
        'losingplayer': x['losingplayer'],
        'generalcontext': x['generalcontext'],
        'specificcontext': x['specificcontext']
    }

client = pymongo.MongoClient(os.getenv('MONGO_URI'))
db = client['TourneyMUs']
collection = db['Matchups']

collection.insert_many(records)