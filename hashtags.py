import pandas as pd
from collections import Counter,OrderedDict
import numpy as np
import sys,os
import numpy as np
path = os.path.dirname(os.path.realpath(__file__))

def split_hashtags(hash_tags,split_s = "|"):
    if isinstance(hash_tags,(float)):
        return []

    hash_tags_list = [tag.strip() for tag in str(hash_tags).split(split_s)]
    return hash_tags_list

def generate_counter(data):
    hash_tags_list = []
    for hash_tags in data['entities_hashtags_list']:
        # print(list(hash_tags))/
        hash_tags_list += list(hash_tags)
    return list(hash_tags_counter(hash_tags_list))

def hash_tags_counter(hash_tags_list):
    # print(hash_tags_list)
    hash_tags_dict = dict(Counter(hash_tags_list))
    hash_tags_data =  pd.DataFrame(hash_tags_dict,index=[0]).T.reset_index()
    hash_tags_data.columns = ['hash_tags',"count"]
    hash_tags_data = hash_tags_data.sort_values(by=['count'],ascending=False)
    # hash_tags_data['hash_tags'] = map(lambda x: x.decode('utf8'), hash_tags_data['hash_tags'])
    hash_tags_data.to_excel(path+"/output/hash_tags.xlsx",index=False)
    hash_tags_dict = {}
    for i,tag in enumerate(hash_tags_data['hash_tags']):
        hash_tags_dict[tag] = i
    return hash_tags_dict,hash_tags_data['count'].values

def generateMatrix(hash_tags):
    hash_tags_list = split_hashtags(hash_tags) if hash_tags else []
    max_tags = len(hash_tags_dict)
    temp = np.zeros(max_tags)
    for num in hash_tags_list:
        # print (num)
        temp[hash_tags_dict.get(num)] = 1
    return temp

def code2(text):
    if isinstance(text,(float)):
        return text
    return text#.decode('utf8')

def arrayToStr(array):
    array = [str(int(ar)) for ar in array]
    return ",".join(array)

if __name__ == '__main__':
    data = pd.read_csv(path+"/data/tweepy_data.csv")
    data2 = pd.read_excel(path+"/output/feather.xlsx")
    data2 = pd.DataFrame(data2.T).reset_index()
    data2.columns = ["user_id",'feather']
    print (data2)
    data.drop_duplicates(inplace=True)
    data.rename(index=str,columns={"user_screen_name":"screen_name"},inplace=True)
    data['entities_hashtags'] = list(map(lambda x:code2(x), data['entities_hashtags']))
    data['entities_hashtags_list'] = list(map(lambda x:split_hashtags(x) if x else [],data['entities_hashtags']))
    hash_tags_dict,count_matrix = generate_counter(data)
    data.drop("entities_hashtags_list",axis=1,inplace=True)
    data['maxtrix'] = list(map(lambda x:generateMatrix(x),data['entities_hashtags']))
    data['hash_tags_v'] = list(map(lambda x:x.dot(count_matrix),data['maxtrix']))
    data['maxtrix'] =list(map(lambda x:arrayToStr(x),data['maxtrix']))
    data[["id","entities_hashtags","maxtrix","hash_tags_v","user_id"]].to_excel(path+"/output/temp.xlsx",index=False)
    data = data.merge(data2,left_on='screen_name',right_on='user_id',how='left')
    data[["hash_tags_v","feather"]].fillna(0).to_excel(path+"/output/feather_hash_v.xlsx",index=False,header=False)
    data[["hash_tags_v", "feather"]].fillna(0).to_excel(path + "/output/feather_hash_Y.xlsx", index=False)
    print (data.head())