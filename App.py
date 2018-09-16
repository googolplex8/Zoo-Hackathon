from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import json

import requests

import tweet_search

app = Flask(__name__)
api = Api(app)


@app.route("/keyword")
def getKeyword(keyword):
    return "obtain keyword"


@app.route("/attributes")
def getAttributes(attributes):
    return "obtain attributes"


@app.route("/data", methods=['GET'])
def postData():
    print("POSTING DATA")
    #API_ENDPOINT = "http:/limitless-sierra-70732.herokuapp.com/postData/"
    data = tweet_search.TweetSearch(getKeyword(), getAttributes())
    json_string = json.dumps(data)
    return jsonify({'tasks': 'datas'})
    #r = requests.post(url=API_ENDPOINT, data=json_string)


def index():
    return "Hello, World!"


if __name__ == '__main__':
    app.run()


