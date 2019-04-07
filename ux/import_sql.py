import json
import psycopg2

conn = psycopg2.connect(
    user='postgres',
    password='postgres',
    host='metabase.potatoes.alxs.dev',
    port=5432,
    database='tweets'
)


def yield_file():
    with open('./diabetes_tweets.json') as file:
        for record in file:
            yield record


def prepare():
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS public.tweets (
        id varchar NOT NULL,
        tweet varchar NOT NULL,
        created_at timestamptz NOT NULL,
        user_id varchar NOT NULL,
        user_name varchar NOT NULL,
        user_login varchar NOT NULL,
        user_location varchar NULL,
        hashtags json NOT NULL,
        sentiment_score int NOT NULL DEFAULT 0,
        CONSTRAINT tweets_pk PRIMARY KEY (id)
    );
    """)


def load():
    cursor = conn.cursor()

    for line in yield_file():
        tweet = json.loads(line)

        location = tweet['user']['location']
        if location is not None:
            location = (tweet['user']['location'] or '') \
                .lower() \
                .replace(',sverige', '').replace(', sverige', '') \
                .replace(',sweden', '').replace(', sweden', '') \
                .strip()

        cursor.execute("""
        INSERT INTO "tweets" (id, tweet, created_at, user_id, user_name, user_login, user_location, hashtags) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (
            tweet['id'],
            tweet['text'],
            tweet['created_at'],
            tweet['user']['id'],
            tweet['user']['name'],
            tweet['user']['screen_name'],
            location,
            '[]'
        ))

        conn.commit()


def load_sentiment():
    cursor = conn.cursor()

    with open('sentiment_scores.json') as sentiment:
        line = sentiment.readline()
        scores = json.loads(line)

        for pair in scores:
            tweet_id, score = pair
            cursor.execute("""UPDATE tweets SET sentiment_score='%s' WHERE id='%s'""", (score, tweet_id))
            conn.commit()


prepare()
# load()
load_sentiment()
