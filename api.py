import os
import json
import pymongo
import flask
from flask import Flask
from flask import request, Response
from bson import json_util
app = Flask(__name__)


client = pymongo.MongoClient(
    "mongodb+srv://numadic:palashshah@bbc.u2vxe.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['bbcdatabase']
# define collection
collection = db['bbcarticles']


@app.route("/", methods=['POST'])
def retrieve_document():
    req_data = request.data.decode("utf-8")
    return json.loads(json_util.dumps({'result' : [post for post in collection.find({'heading': {'$regex': req_data}})]}))


if __name__ == '__main__':
    app.run()
