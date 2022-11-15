from flask import Flask, Response, redirect, request, render_template, flash
from lists import *
import pymongo
import os

app = Flask(__name__)
app.secret_key = 'better lucky than good'

client = pymongo.MongoClient(os.getenv('MONGO_URI'))
db = client['TourneyMUs']
collection = db['Matchups']
num_records: int = len(list(collection.find({})))
print(num_records)
@app.route('/', methods=['GET', 'POST'])
def upload_record():
    if request.method == 'GET':
        return render_template('index.html', players=PLAYERS, decks=DECKS, tournaments=TOURNAMENTS, message='', default=DEFAULTS)
    else:
        client = pymongo.MongoClient(os.getenv('MONGO_URI'))
        db = client['TourneyMUs']
        collection = db['Matchups']
        num_records: int = len(list(collection.find({})))
        print(num_records)
        docs: list=[]
        for i in range(int(request.form.get("Wins"))):
            docs.append({
            '_id': num_records+1,
            'winningplayer':request.form.get('winning_player'),
            'losingplayer':request.form.get('losing_player'),
            'winningMC':request.form.get('winningMC'),
            'losingMC':request.form.get('losingMC'),
            'generalcontext':TOURNAMENTS[request.form.get('Tournament')],
            'specificcontext':request.values.get('Tournament')
        })
            num_records = num_records+1

        for i in range(int(request.form.get("Losses"))):
            docs.append({
            '_id': num_records+1,
            'winningplayer':request.form.get('losing_player'),
            'losingplayer':request.form.get('winning_player'),
            'winningMC':request.form.get('losingMC'),
            'losingMC':request.form.get('winningMC'),
            'generalcontext':TOURNAMENTS[request.form.get('Tournament')],
            'specificcontext':request.values.get('Tournament')
        })
            num_records = num_records+1
        
        msg=f'Updated records. Last id: {num_records}'
        try:
            collection.insert_many(docs)
        except:
            msg= 'Connection error.'
        
        return render_template('index.html', players=PLAYERS, decks=DECKS, tournaments=TOURNAMENTS, message=msg, default={
            'winningplayer':request.form.get('winning_player'),
            'losingplayer':request.form.get('losing_player'),
            'winningMC':request.form.get('winningMC'),
            'losingMC':request.form.get('losingMC'),
            'tour':request.form.get('Tournament'),
            'Wins':request.form.get("Wins"),
            'Losses':request.form.get('Losses')
        })

if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)