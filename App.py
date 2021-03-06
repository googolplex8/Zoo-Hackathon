from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import json
import requests

import tweet_search

app = Flask(__name__)
api = Api(app)
keyword = ""
attributes = [None, None, None]

def setKeyword(in_keyword):
    keyword = in_keyword
    return "obtained keyword"


def setAttributes(in_attributes):
    attributes = in_attributes
    return "obtained attributes"


def postData():
    print("POSTING DATA")
    #API_ENDPOINT = "http:/limitless-sierra-70732.herokuapp.com/postData/"
    # r = requests.post(url=API_ENDPOINT, data=json_string)
    data = tweet_search.TweetSearch(keyword, attributes)
    json_string = json.dumps(data)
    return json_string


def index():
    return "Hello, World!"


if __name__ == '__main__':
    app.run()


