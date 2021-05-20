# coding: UTF-8
import os
import json
from requests_oauthlib import OAuth1Session
from datetime import datetime, timedelta, timezone
import logging

# ログ設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Twitter検索パラメータ
JST = timezone(timedelta(hours=+9), 'JST')
CK = os.environ['TWITTER_CONSUMER_KEY'] # * enter your Consumer Key *
CS = os.environ['TWITTER_CONSUMER_SECRET'] # * enter your Consumer Secret *
AT = os.environ['TWITTWR_ACCESS_TOKEN'] # * enter your Access Token *
AS = os.environ['TWITTWR_ACCESS_TOKEN_SECRET'] # * enter your Accesss Token Secert *
twitter = OAuth1Session(CK, CS, AT, AS)

def scrape_twitter_with_keyword():
    keywords = '\"強化学習\" OR \"マルチエージェント\"'
    return search_tweet(keywords)

def search_tweet(keywords):
    now = datetime.now(JST).strftime('%Y-%m-%d_%H:00:00_JST')
    one_day_before = (datetime.now(JST) - timedelta(days=1)).strftime('%Y-%m-%d_%H:00:00_JST')
    query_str = keywords + " " \
    "since:" + one_day_before + " "\
    "until:" + now    
    logging.info('検索条件: ' + query_str)
    
    params = {
        "q": query_str,
        "count": 10
    }
    twitter_search_url = 'https://api.twitter.com/1.1/search/tweets.json'
    req = twitter.get(twitter_search_url, params = params)

    if req.status_code == 200:
        # 取得したtweetsから各ユーザの投稿だけ取り出す
        tweets = json.loads(req.text)['statuses']
        # 返却メッセージの生成
        return_msg = ''
        for line in tweets:
            return_msg += line['text']
            return_msg += '\n\n'
        return return_msg
    else:
        return 'error'

print(scrape_twitter_with_keyword())