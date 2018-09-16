import json
import pandas as pd
import matplotlib.pyplot as plt
import re
import operator

def main(keyword, associations):
    #Reading Tweets
    print('Reading Tweets\n')
    tweets_data_path = 'twitter_data.txt'

    tweets_data = []
    tweets_file = open(tweets_data_path, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        except:
            continue

    #Structuring Tweets
    print('Structuring Tweets\n')
    tweets = pd.DataFrame()
    tweets['text'] = list(map(lambda tweet: tweet['text'], tweets_data))
    scored_tweets = {}
    for tweet in tweets["text"]:
        if word_in_text(keyword, tweet):
            scored_tweets[tweet] = 1

    for key in scored_tweets:
        for i in range(len(associations)):
            if word_in_text(associations[i], key):
                scored_tweets[key] +=1

    sorted_scores = sorted(scored_tweets.items(), key=operator.itemgetter(1), reverse=True)

    print(len(tweets["text"]))
    print(len(scored_tweets))
    print(len(sorted_scores))
    for scored_pair in sorted_scores:
        print(scored_pair[0])


def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False


if __name__ == '__main__':
    main("medicine", ["ivory", "tusk", "head"])
