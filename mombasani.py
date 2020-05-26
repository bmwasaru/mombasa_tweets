from __future__ import unicode_literals
import os
import json
import logging
import time

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, API
from tweepy import Stream
import psycopg2

access_token = os.environ.get('access_token')
access_token_secret = os.environ.get('access_token_secret')
consumer_key = os.environ.get('consumer_key')
consumer_secret = os.environ.get('consumer_secret')

db = psycopg2.connect(
    host="localhost",
    user=os.environ.get('user'),
    password=os.environ.get('passwd'),
    dbname="mombasani"
)

db_cursor = db.cursor()

auth_handler = OAuthHandler(consumer_key, consumer_secret)
auth_handler.set_access_token(access_token, access_token_secret)

api = API(auth_handler)


class TweetsListener(StreamListener):
    def on_data(self, data):
        tweet = json.loads(data)
        sql = "INSERT INTO tweets (tweet_id, tweet_text) VALUES (%s, %s)"
        values = (tweet['id'], tweet['text'])
        db_cursor.execute(sql, values)
        return True

    def on_error(self, status):
        logging.error("Status: {}".format(status))


if __name__ == '__main__':
    try:
        listener = TweetsListener()
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth, listener)
        stream.filter(track=['mombasa'])
    except Exception as e:
        print(e)
        time.sleep(3600)
