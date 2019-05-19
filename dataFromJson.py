import json
import os,sys
import pandas as pd
import codecs
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

path = os.path.dirname(os.path.realpath(__file__))
base_path = path+"/"+"germanwings-crash-all-rnr-threads/rumours"
id_file_list = os.listdir(base_path)
if __name__ == "__main__":
    total_pd = pd.DataFrame()
    for id in id_file_list[:]:
        if "." not in id :
            # print(id)
            file_name = os.listdir(base_path+"/"+id+"/"+"source-tweets")[1]
            print(file_name)
            try:
                with codecs.open(base_path+"/"+id+"/"+"source-tweets/"+file_name,encoding='GBK') as fp:
                    temp_json_str =  ''.join(fp.readlines())
                    print(temp_json_str)
            except:
                continue
            temp_pd =  extractJson(json.loads(temp_json_str))
            total_pd = pd.concat([total_pd,temp_pd],axis=0)
    total_pd.to_csv(path+"/data/tweepy_data.csv",index=False, encoding='utf8',mode="a+",header=False)
