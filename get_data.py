import os
import sys
import datetime

import pandas as pd 
import snscrape.modules.twitter as sntwitter

def make_file(tweets,keyword,target_path):
    date = str(datetime.datetime.now().date())
    tweet_df = pd.DataFrame(tweets,columns=['date','url','rawContent','id','username',
    'replyCount','likeCount','retweetCount','quoteCount','viewCount'])
    filename = keyword +'_tweets_'+ date +'.csv'
    path = os.path.join(target_path,filename) 
    tweet_df.to_csv(path,index=False)

def scrape_data(keyword):
    scraper = sntwitter.TwitterSearchScraper( '#'+keyword)
    tweets = []
    for i, tweet in enumerate(scraper.get_items()):
        data = [
            tweet.date,
            tweet.url,
            tweet.rawContent,
            tweet.id,
            tweet.user.username,
            tweet.replyCount,
            tweet.likeCount,
            tweet.retweetCount,
            tweet.quoteCount,
            tweet.viewCount
        ]
        tweets.append(data)
        # get 5000 tweets
        if i > 5000:
            break
    return tweets




def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def main(category,keywords):
    cwd = os.getcwd()
    target_path = os.path.join(cwd,'data',f"{category}_data")
    create_dir(target_path)
    
    for keyword in keywords:
        tweets =  scrape_data(keyword)
        make_file(tweets,keyword,target_path)

if __name__ == "__main__":
     args = sys.argv
     if len(args) < 3:
        raise Exception("You must pass a category and a keyword - get_data.py #category #keywords")
     category = args[1]
     keywords = args[2:]
     main(category,keywords)