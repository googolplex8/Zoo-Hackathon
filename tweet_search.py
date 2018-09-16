import json
import pandas as pd
import re
import operator


class TweetSearch:
    def load_tweets(self):
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
        package = (tweets['text'], tweets ['country'])
        return package


    def search_by_keyword(self, tweets, keyword):
        scored_tweets = {}
        for tweet in tweets:
            if self.word_in_text(keyword, tweet):
                scored_tweets[tweet] = 1

        print(len(tweets))
        print(len(scored_tweets))
        return scored_tweets


    def narrow_down_by_associations(self, scored_tweets, associations):
        for key in scored_tweets:
            for i in range(len(associations)):
                if key is not None and self.word_in_text(associations[i], key):
                    scored_tweets[key] +=1
        sorted_scores = sorted(scored_tweets.items(), key=operator.itemgetter(1), reverse=True)
        for scored_pair in sorted_scores:
            print(scored_pair[0])
        return sorted_scores

    def narrow_down_by_location(self, tweets, location):
        location_sorted = []
        for loc in tweets:
            if loc is not None:
                print(loc)
        return tweets


    def word_in_text(self, word, text):
        word = word.lower()
        text = text.lower()
        match = re.search(word, text)
        if match:
            return True
        return False

    def __init__(self, keyword, attributes):
        tweets_and_loc = self.load_tweets()
        tweets = self.search_by_keyword(tweets_and_loc[0], keyword)
        #xx = self.narrow_down_by_location(tweets_and_loc[1], "US")
        tweets = self.narrow_down_by_associations(tweets, [attributes[0], attributes[1], attributes[2]])

