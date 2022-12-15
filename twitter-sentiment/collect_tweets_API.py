# based on tutorial - Andrew Edward:
# An Extensive Guide to collecting tweets from Twitter API v2 for academic research using Python 3
# https://towardsdatascience.com/an-extensive-guide-to-collecting-tweets-from-twitter-api-v2-for-academic-research-using-python-3-518fcb71df2a



import requests
import os
import json
import pandas as pd
import csv
import datetime
import dateutil.parser
import unicodedata
import time




os.environ['TOKEN'] = "..enter your bearer token here..."

#---------------------------------------

#---------------------------------------
def auth():
    return os.getenv('TOKEN')
#---------------------------------------

#---------------------------------------
def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers
#---------------------------------------

#---------------------------------------
def create_url(keyword, start_date, end_date, max_results = 10):
    search_url = "https://api.twitter.com/2/tweets/search/all"
    query_params = {'query': keyword,
                    'start_time': start_date,
                    'end_time': end_date,
                    'max_results': max_results,
                    'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
                    'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
                    'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
                    'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
                    'next_token': {}}
    return (search_url, query_params)
#---------------------------------------

#---------------------------------------
def connect_to_endpoint(url, headers, params, next_token = None):
    params['next_token'] = next_token   #params object received from create_url function
    response = requests.request("GET", url, headers = headers, params = params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()
#---------------------------------------

#---------------------------------------
def append_to_csv(json_response, fileName):
    counter = 0

    csvFile = open(fileName, "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)

    for tweet in json_response['data']:
        
        # We will create a variable for each since some of the keys might not exist for some tweets
        author_id = tweet['author_id']

        created_at = dateutil.parser.parse(tweet['created_at'])

        if ('geo' in tweet):
            try:
                geo = tweet['geo']['place_id']
            except:
                geo = " "
        else:
            geo = " "

        tweet_id = tweet['id']
        lang = tweet['lang']
        retweet_count = tweet['public_metrics']['retweet_count']
        reply_count = tweet['public_metrics']['reply_count']
        like_count = tweet['public_metrics']['like_count']
        quote_count = tweet['public_metrics']['quote_count']
        source = tweet['source']
        text = tweet['text']
        
        res = [author_id, created_at, geo, tweet_id, lang, like_count, quote_count, reply_count, retweet_count, source, text]
        
        csvWriter.writerow(res)
        counter += 1

    csvFile.close()

    print("# of Tweets added from this response: ", counter) 
#---------------------------------------

#---------------------------------------



bearer_token = auth()
headers = create_headers(bearer_token)

keyword = "pedagogique"
filename_keyw = "pedag"




start_list =    ['2022-01-01T00:00:00.000Z',
                 '2022-02-01T00:00:00.000Z',
                 '2022-03-01T00:00:00.000Z',
                ]

end_list =      ['2022-01-31T00:00:00.000Z',
                 '2022-02-28T00:00:00.000Z',
                 '2022-03-31T00:00:00.000Z',
                 ]


max_results = 500 # max 500 (per 'page')


total_tweets = 0 #Total number of tweets we collected from the loop


year = '2022'

curr_dir = os.getcwd()
fileout_pref = curr_dir + str(year) + "/tw_" + filename_keyw + "_" + str(year)

for i in range(0, len(start_list)):

    curr_csvfile = fileout_pref + "_mth_" + str(i) + ".csv"
    #curr_csvfile = fileout_pref + ".csv"

    print("will save to ", curr_csvfile)
    csvFile = open(curr_csvfile, "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(['author id', 'created_at', 'geo', 'id','lang', 'like_count', 'quote_count', 'reply_count','retweet_count','source','tweet'])
    csvFile.close()



    print("Month: ", str(i))
    count = 0
    max_count = 100000 # Max tweets per time period
    flag = True
    next_token = None
    
    while flag:
        if count >= max_count:
            break
        print("-------------------")
        print("Token: ", next_token)
        url = create_url(keyword, start_list[i],end_list[i], max_results)
        json_response = connect_to_endpoint(url[0], headers, url[1], next_token)

        result_count = json_response['meta']['result_count']

        if 'next_token' in json_response['meta']:
            next_token = json_response['meta']['next_token']
            print("Next Token: ", next_token)
            if result_count is not None and result_count > 0 and next_token is not None:
                print("Start Date: ", start_list[i])
                append_to_csv(json_response, curr_csvfile)
                count += result_count
                total_tweets += result_count
                print("Total # of Tweets added: ", total_tweets)
                print("-------------------")
                time.sleep(5)                
        else:
            if result_count is not None and result_count > 0:
                print("-------------------")
                print("Start Date: ", start_list[i])
                append_to_csv(json_response, curr_csvfile)
                count += result_count
                total_tweets += result_count
                print("Total # of Tweets added: ", total_tweets)
                print("-------------------")
                time.sleep(5)
            
            flag = False
            next_token = None
        time.sleep(5)
    print("Done.")
print("Total number of results: ", total_tweets)
