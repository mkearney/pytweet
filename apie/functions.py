
import urllib.parse
import pandas as pd
import numpy as np
import oauth2
import os
import json

TWITTER_PAT = os.environ.get('TWITTER_PAT', None)

class APIKeyMissingError(Exception):
  pass


if TWITTER_PAT is None:
  raise APIKeyMissingError(
    "All methods require an API key. See "
    "https://developer.twitter.com "
    "for how to retrieve an authentication token from "
    "Twitter's APIs"
  )

with open(TWITTER_PAT, 'r') as f:
  keys = json.load(f)


def twitter_api_get(url):
    url = 'https://api.twitter.com/1.1/' + url
    consumer = oauth2.Consumer(key=keys.get('app').get('key'), secret=keys.get('app').get('secret'))
    token = oauth2.Token(key=keys.get('credentials').get('oauth_token'), secret=keys.get('credentials').get('oauth_token_secret'))
    client = oauth2.Client(consumer, token)
    resp, content = client.request(url, method="GET")
    print('# Response status code: ' + resp.get('status'))
    return json.loads(content)


def get_home_timeline():
    return twitter_api_get('statuses/home_timeline.json')

def search_tweets_(query, n = 100):
    query = urllib.parse.quote(query)
    res = twitter_api_get('search/tweets.json?q=' + query + '&count=' + str(n))
    return pd.DataFrame(res['statuses'])

#[{'id_str', 'created_at', 'screen_name', 'text'}]

def search_tweets(query, n = 100):
    n = int(np.ceil(n / 100))
    out = pd.DataFrame()
    for i in range(n):
        out = out.append(search_tweets_(query, n = 100))
    return out
