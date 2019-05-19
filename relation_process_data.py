import pandas as pd
import tweepy
import time
import os,sys

consumerKey = "CESb19sOylnUOJ9tX0YikIOfD"
consumerSecret = "dvIfInJTcSOKXLm7pmEEEaFqggH4HAYZceFBMZYvmiYtHwIdpd"
accessToken = "1024491310286131200-y2Eyh47kyHxrNZRvTVl6bOkyJF9n8O"
accessTokenSecret = "emkjv06TTTphm37l4umfR1XuRMtxm6NaRRY1VWk1LjClE"

# Setup tweepy to authenticate with Twitter credentials:
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
# Create the api to connect to twitter with your creadentials
get_api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

path = os.path.dirname(os.path.realpath(__file__))

class ProcessData(object):
    def __init__(self):
        self.api = get_api

    def get_follow(self,data_df):
        """#Following Relationship, A follows B is 1  other is 0"""
        for user_1 in data_df['screen_name']:
            for user_2 in data_df['screen_name']:
                is_follow = 0
                if user_1 == user_2:
                    continue
                try:
                    status = self.api.show_friendship(source_screen_name=user_1, target_screen_name=user_2)
                    print(status)
                    if status[0].following:
                        is_follow = 1
                    with open(path+'/output/following.csv', 'a') as f:
                        f.write('{},{},{}\n'.format(user_1, user_2, is_follow))
                except Exception as e:
                    print(e)


if __name__ == '__main__':
    data = pd.read_csv(path+"/data/tweepy_data.csv")
    data.drop_duplicates(inplace=True)
    data.rename(index=str,columns={"user_screen_name":"screen_name"},inplace=True)
    data = pd.DataFrame(data['screen_name'].value_counts()).reset_index()
    data.columns = ["screen_name","count"]
    data = data[data['screen_name'] !="user_screen_name"]
    process_data = ProcessData()
    # Following Relationship, A follows B is 1  other is 0
    process_data.get_follow(data)
