import psycopg2
import tweepy
import re

from textblob import TextBlob


class DataBase():
    def __init__(self, host, database, user, password):
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )

        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tweets (
                id BIGINT PRIMARY KEY,
                keyword TEXT NOT NULL,
                tweet_text TEXT NOT NULL,
                author VARCHAR(50) NOT NULL,
                twitter_name VARCHAR(50) NOT NULL,
                tweet_url VARCHAR(100) NOT NULL,
                rt_count INTEGER NOT NULL,
                fav_count INTEGER NOT NULL,
                created_at date NOT NULL,
                subjectivity REAL  NOT NULL,
                polarity REAL NOT NULL,
                analysis VARCHAR(10) NOT NULL
            );
        """)
        self.conn.commit()
        cursor.close()

    def data_to_table(self, tweet_id, keyword, tweet_text, rt_count, fav_count,
                      author, twitter_name, tweet_url, created_at,
                      subjectivity, polarity, analysis):
        cursor = self.conn.cursor()
        cursor.execute(
            """
                INSERT INTO tweets 
                    (id, keyword, tweet_text, author, twitter_name, tweet_url,
                    rt_count, fav_count, created_at, subjectivity,
                    polarity, analysis) 
                    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
                ON CONFLICT (id) DO UPDATE SET
                    rt_count = %s,
                    fav_count = %s;
            """, (tweet_id, keyword, tweet_text, author, twitter_name, tweet_url,
                  rt_count, fav_count, created_at, subjectivity,
                  polarity, analysis, rt_count, fav_count))
        self.conn.commit()
        cursor.close()


class Twitter():
    def __init__(self, api_key, api_key_secret,
                 access_token, access_token_secret):
        # Twitter authentication
        auth = tweepy.OAuthHandler(api_key, api_key_secret)
        auth.set_access_token(access_token, access_token_secret)

        # Creating an API object
        self.api = tweepy.API(auth)

    def search_tweets(self, keyword, result_type="popular", lang="en"):
        return tweepy.Cursor(self.api.search_tweets, q=keyword,
                             result_type=result_type, lang=lang).items()


class SentimentAnalysis():
    def clean_tweet(tweet):
        tweet = re.sub(r"@[A-Za-z0-9]", "", tweet)  # Remove @mentions
        tweet = re.sub(r"#", "", tweet)  # Remove '#' symbol
        tweet = re.sub(r"RT[\s]+", "", tweet)  # Remove RT
        tweet = re.sub(r"https?:\/\/\S+", "", tweet)  # Remove the hyper link
        tweet = re.sub(r"[\t\n\r]+", "", tweet)  # Remove spaces
        return tweet

    def analyze_polarity(polarity):
        if polarity < 0:
            return 'NEGATIVE'
        elif polarity == 0:
            return 'NEUTRAL'
        else:
            return 'POSITIVE'

    def polarity(text):
        return TextBlob(text).sentiment.polarity

    def subjectivity(text):
        return TextBlob(text).sentiment.subjectivity
