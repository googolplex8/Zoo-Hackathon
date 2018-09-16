import json
import pandas as pd
import re
import operator


def load_tweets():
    # Reading Tweets
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

    # Structuring Tweets
    print('Structuring Tweets\n')
    tweets = pd.DataFrame()
    tweets['country'] = list(
        map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data))
    tweets['text'] = list(map(lambda tweet: tweet['text'], tweets_data))

    package = []
    i = 0
    for tweet in tweets["country"]:
        if tweets["country"] is not None:
            print(tweet['place'])

    for loc in tweets['country']:
        if loc is not None:
            package.append([None, loc])
            i = i + 1

    print(i)
    return package


def search_by_keyword(tweets, keyword):
    scored_tweets = {}
    for tweet in tweets:
        if word_in_text(keyword, tweet):
            scored_tweets[tweet] = 1

    print(len(tweets))
    print(len(scored_tweets))
    return scored_tweets


def narrow_down_by_associations(scored_tweets, associations):
    for key in scored_tweets:
        for i in range(len(associations)):
            if key is not None and word_in_text(associations[i], key):
                scored_tweets[key] +=1
    sorted_scores = sorted(scored_tweets.items(), key=operator.itemgetter(1), reverse=True)
    #for scored_pair in sorted_scores:
        #print(scored_pair[0])
    return sorted_scores

def narrow_down_by_location(tweets, location):
    location_sorted = []
    for loc in tweets:
        if loc is not None:
            print(loc)
    return tweets


def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False


if __name__ == '__main__':
    tweets_and_loc = load_tweets()
    #tweets = search_by_keyword(tweets_and_loc[0], "medicine")
    #xx = narrow_down_by_location(tweets_and_loc[1], "US")
    #tweets = narrow_down_by_associations(tweets, ["ivory", "tusk", "keratin"])

