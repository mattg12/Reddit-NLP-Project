# Reddit Data Scraping
# Script to pull posts from subreddits using Reddit's API
# Matthew Garton - September 7, 2018
# General Assembly - Data Science Immersive

# import necessary modules
import requests
import json
import time
import pandas as pd
import datetime

# instantiate needed URLS
url_dc = 'http://www.reddit.com/r/DCcomics.json'
url_marvel = 'https://www.reddit.com/r/Marvel.json'

# set my header
my_header = {'User-agent': 'Matt Garton'}

def get_reddit_data(urls, header, size = 1000):
    '''Returns a dataframe of posts from a given list of subreddits'''
    
    posts = []
    after = None
    
    for u in urls: # iterate over urls passed to function
        for _ in range(size): # loop the desired number of times
            if after == None:
                params = {}
            else:
                params = {'after': after}
                
            res = requests.get(u, params = params, headers = header) # get the data
            
            if res.status_code == 200: # add data to posts if request succeeds
                the_json = res.json()
                post = [p['data'] for p in the_json['data']['children']]
                posts.extend(post)
                if the_json['data']['after'] == None:
                    continue
                else:
                    after = the_json['data']['after'] # update after
            else:
                print(res.status_code) # break and provide feedback if request fails
                break
                
            time.sleep(1) # pause
        
    df = pd.DataFrame(posts)
    
    now = datetime.datetime.now()
    df.to_csv('./data/reddit_data_{}{}{}_{}:{}:{}'.format(now.year, now.month, now.day, now.hour, now.minute, now.second))
    return df

get_reddit_data(urls = [url_dc, url_marvel], header = my_header)