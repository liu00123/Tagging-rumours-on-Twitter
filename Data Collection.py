# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the tweepy librarytweepy
import tweepy
import pandas as pd
import os,sys

path = os.path.dirname(os.path.realpath(__file__))
# Variables that contains the user credentials to access Twitter API
def extractJson(json_data):
    tweet = json_data
    data = {}
    if 'text' in tweet:  # only messages contains 'text' field is a tweet
        data['id'] = tweet['id'] # This is the tweet's id
        data['create_at'] = tweet['created_at'] # when the tweet posted
        data['text'] = tweet['text']  # content of the tweet

        data['user_id'] = tweet['user']['id'] # id of the user who posted the tweet
        data['user_name'] = tweet['user']['name']  # name of the user, e.g. "Wei Xu"
        data['user_screen_name'] = tweet['user']['screen_name']  # name of the user account, e.g. "cocoweixu"

        hashtags = []
        for hashtag in tweet['entities']['hashtags']:
            hashtags.append(hashtag['text'])
        data['entities_hashtags'] = " | ".join(hashtags)
    return pd.DataFrame(data,index=['0'])


consumerKey = "CESb19sOylnUOJ9tX0YikIOfD"
consumerSecret = "dvIfInJTcSOKXLm7pmEEEaFqggH4HAYZceFBMZYvmiYtHwIdpd"
accessToken = "1024491310286131200-y2Eyh47kyHxrNZRvTVl6bOkyJF9n8O"
accessTokenSecret = "emkjv06TTTphm37l4umfR1XuRMtxm6NaRRY1VWk1LjClE"

# Setup tweepy to authenticate with Twitter credentials:

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)

# Create the api to connect to twitter with your creadentials
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)


# Print the result
if __name__ == "__main__":
    total_result = pd.DataFrame()
    i = 1
    places = api.geo_search(query="Australia", granularity="country")
    maxTweets = 100
    searchQuery = 'place:' + places[0].id
    # for status in tweepy.Cursor(api.home_timeline).items(maxTweets):
    #     temp = extractJson(status._json)
    #             if i == 1:
    #                 temp.to_csv(path+"/data/tweepy_data.csv",encoding='utf8',mode='w+)
    #             else:
    #                 temp.to_csv(path+"/data/tweepy_data.csv", encoding='utf8',header=None,mode='a)
    #             i += 1
    for tweet in tweepy.Cursor(api.search, q=searchQuery).items(maxTweets):
        if tweet.place is not None:
            temp = extractJson(tweet._json)
            print(temp)
            if i == 1:
                temp.to_csv(path+"/data/tweepy_data.csv", encoding='utf8',mode='w+')
            else:
                temp.to_csv(path+"/data/tweepy_data.csv", encoding='utf8', header=None,mode="a")
            i += 1

