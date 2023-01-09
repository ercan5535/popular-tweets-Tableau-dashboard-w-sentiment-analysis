import credentials

from helper import DataBase, Twitter, SentimentAnalysis


# Get Twitter API credentials
API_KEY = credentials.api_key
API_KEY_SECRET = credentials.api_key_secret
ACCESS_TOKEN = credentials.access_token
ACCES_TOKEN_SECRET = credentials.access_token_secret

# Get Database credentials
HOST = credentials.host
DB_NAME = credentials.db_name
USERNAME = credentials.username
PASSWORD = credentials.password

# Get Keywords
KEYWORDS = credentials.keywords

# Connect Postgresql db
db_operations = DataBase(
    host=HOST,
    database=DB_NAME,
    user=USERNAME,
    password=PASSWORD
)

# Connect Twitter api
twitter = Twitter(API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCES_TOKEN_SECRET)

# Search for tweets containing the keyword in KEYWORDS
for keyword in KEYWORDS:
    tweets = twitter.search_tweets(keyword)

    for tweet in tweets:
        # Parsee tweet object
        tweet_id = tweet.id
        tweet_text = tweet.text
        rt_count = tweet.retweet_count
        fav_count = tweet.favorite_count
        author = tweet.user.name
        twitter_name = tweet.user.screen_name
        tweet_url = r"https://twitter.com/twitter/statuses/" + str(tweet.id)
        created_at = tweet.created_at.strftime("%d/%m/%Y, %H:%M:%S")

        # Sentiment analysis
        clean_tweet = SentimentAnalysis.clean_tweet(tweet_text)
        polarity = SentimentAnalysis.polarity(tweet_text)
        subjectivity = SentimentAnalysis.subjectivity(tweet_text)
        analysis = SentimentAnalysis.analyze_polarity(polarity)

        # Update DB
        db_operations.data_to_table(
            tweet_id, keyword, tweet_text, rt_count, fav_count,
            author, twitter_name, tweet_url, created_at,
            subjectivity, polarity, analysis
        )
