import json
import pandas as pd
import matplotlib.pyplot as plt
import re

def main():
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
    tweets['lang'] = list(map(lambda tweet: tweet['lang'], tweets_data))
    tweets['country'] = list(map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data))


    #Analyzing Tweets by Language
    print('Analyzing tweets by language\n')
    tweets_by_lang = tweets['lang'].value_counts()
    fig, ax = plt.subplots()
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=10)
    ax.set_xlabel('Languages', fontsize=15)
    ax.set_ylabel('Number of tweets' , fontsize=15)
    ax.set_title('Top 5 languages', fontsize=15, fontweight='bold')
    tweets_by_lang[:7].plot(ax=ax, kind='bar', color='red')
    plt.savefig('tweet_by_lang', format='png')


    #Analyzing Tweets by Country
    print('Analyzing tweets by country\n')
    tweets_by_country = tweets['country'].value_counts()
    #print(len(tweets['country'].value_counts()))
    fig, ax = plt.subplots()
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=10)
    ax.set_xlabel('Countries', fontsize=15)
    ax.set_ylabel('Number of tweets' , fontsize=15)
    ax.set_title('Top 5 countries', fontsize=15, fontweight='bold')
    tweets_by_country[:7].plot(ax=ax, kind='bar', color='blue')
    plt.savefig('tweet_by_country', format='png')

    #comparison of particular key words
    tweets['ivory'] = tweets['text'].apply(lambda tweet: word_in_text('ivory', tweet))
    tweets['tusk'] = tweets['text'].apply(lambda tweet: word_in_text('tusk', tweet))
    tweets['pangolin'] = tweets['text'].apply(lambda tweet: word_in_text('pangolin', tweet))
    print(tweets['ivory'].value_counts()[True])
    print(tweets['tusk'].value_counts()[True])
    print(tweets['pangolin'].value_counts()[True])
    prg_langs = ['ivory', 'tusk', 'pangolin']
    tweets_by_prg_lang = [tweets['ivory'].value_counts()[True], tweets['tusk'].value_counts()[True],
                          tweets['pangolin'].value_counts()[True]]
    x_pos = list(range(len(prg_langs)))
    width = 0.8
    fig, ax = plt.subplots()
    plt.bar(x_pos, tweets_by_prg_lang, width, alpha=1, color='g')
    # Setting axis labels and ticks
    ax.set_ylabel('Number of tweets', fontsize=15)
    ax.set_title('Ranking: ivory vs. tusk vs. pangolin (Raw data)', fontsize=10, fontweight='bold')
    ax.set_xticks([p + 0.4 * width for p in x_pos])
    ax.set_xticklabels(prg_langs)
    plt.grid()

    #relevancy
    tweets['medicine'] = tweets['text'].apply(lambda tweet: word_in_text('medicine', tweet))
    tweets['sale'] = tweets['text'].apply(lambda tweet: word_in_text('sale', tweet))
    tweets['relevant'] = tweets['text'].apply(lambda tweet: word_in_text('medicine', tweet) or word_in_text('sale', tweet))
    print(tweets['medicine'].value_counts()[True])
    print(tweets['sale'].value_counts()[True])
    print(tweets['relevant'].value_counts()[True])
    tweets_by_prg_lang = [tweets[tweets['relevant'] == True]['ivory'].value_counts()[True],
                          tweets[tweets['relevant'] == True]['tusk'].value_counts()[True],
                          tweets[tweets['relevant'] == True]['pangolin'].value_counts()[True]]
    x_pos = list(range(len(prg_langs)))
    width = 0.8
    fig, ax = plt.subplots()
    plt.bar(x_pos, tweets_by_prg_lang, width, alpha=1, color='g')
    ax.set_ylabel('Number of tweets', fontsize=15)
    ax.set_title('Ranking: ivory vs. tusk vs. pangolin (Relevant data)', fontsize=10, fontweight='bold')
    ax.set_xticks([p + 0.4 * width for p in x_pos])
    ax.set_xticklabels(prg_langs)
    plt.grid()
    #plt.show()

    for tweet in tweets[tweets['relevant']==True]["text"]:
        print(tweet)


def coordinates():
    fname = 'twitter_data.txt'
    with open(fname, 'r') as f:

        # Create dictionary to later be stored as JSON. All data will be included
        # in the list 'data'
        users_with_geodata = {
            "data": []
        }
        all_users = []
        total_tweets = 0
        geo_tweets = 0
        for line in f:
            print(line)
            try:
                tweet = json.loads(line)
            except:
                continue
            if tweet['user']['id']:
                total_tweets += 1
                user_id = tweet['user']['id']
                if user_id not in all_users:
                    all_users.append(user_id)

                    # Give users some data to find them by. User_id listed separately
                    # to make iterating this data later easier
                    user_data = {
                        "user_id": tweet['user']['id'],
                        "features": {
                            "name": tweet['user']['name'],
                            "id": tweet['user']['id'],
                            "screen_name": tweet['user']['screen_name'],
                            "tweets": 1,
                            "location": tweet['user']['location'],
                        }
                    }
                    # Iterate through different types of geodata to get the variable primary_geo
                    if tweet['coordinates']:
                        user_data["features"]["primary_geo"] = str(
                            tweet['coordinates'][list(tweet['coordinates'].keys())[1]][1]) + ", " + str(
                            tweet['coordinates'][list(tweet['coordinates'].keys())[1]][0])
                        user_data["features"]["geo_type"] = "Tweet coordinates"
                    elif tweet['place']:
                        user_data["features"]["primary_geo"] = tweet['place']['full_name'] + ", " + tweet['place'][
                            'country']
                        user_data["features"]["geo_type"] = "Tweet place"
                    else:
                        user_data["features"]["primary_geo"] = tweet['user']['location']
                        user_data["features"]["geo_type"] = "User location"
                    # Add only tweets with some geo data to .json. Comment this if you want to include all tweets.
                    if user_data["features"]["primary_geo"]:
                        users_with_geodata['data'].append(user_data)
                        geo_tweets += 1

                # If user already listed, increase their tweet count
                elif user_id in all_users:
                    for user in users_with_geodata["data"]:
                        if user_id == user["user_id"]:
                            user["features"]["tweets"] += 1

        # Count the total amount of tweets for those users that had geodata
        for user in users_with_geodata["data"]:
            geo_tweets = geo_tweets + user["features"]["tweets"]
        # Get some aggregated numbers on the data
        print("The file included " + str(len(all_users)) + " unique users who tweeted with or without geo data")
        print("The file included " + str(len(users_with_geodata['data'])) + " unique users who tweeted with geo data, including 'location'")
        print("The users with geo data tweeted " + str(geo_tweets) + " out of the total " + str(total_tweets) + " of tweets.")
    # Save data to JSON file
    with open('twitter_data_geo.txt', 'w') as fout:
        fout.write(json.dumps(users_with_geodata, indent=4))


def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False


if __name__ == '__main__':
    main()
    #coordinates()

