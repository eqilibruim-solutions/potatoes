import json
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://metabase.potatoes.alxs.dev:7687", auth=("neo4j", "neo4j1"))


def yield_file():
    with open('./diabetes_tweets.json') as file:
        for record in file:
            yield record


def load():
    session = driver.session()
    session.write_transaction(prepare)

    for line in yield_file():
        tweet = json.loads(line)
        session.write_transaction(create_tweet, tweet)


def prepare(tx):
    tx.run("CREATE CONSTRAINT ON (h:Hashtag) ASSERT h.text IS UNIQUE")
    tx.run("CREATE CONSTRAINT ON (u:User) ASSERT u.id IS UNIQUE")
    tx.run("CREATE CONSTRAINT ON (t:Tweet) ASSERT t.id IS UNIQUE")
    tx.run("CREATE CONSTRAINT ON (l:Location) ASSERT l.name IS UNIQUE")


def create_tweet(tx, tweet):
    """
    create_tweet transforms JSON tweet into parts and relations of neo4j graph
    """

    tweet_id = tweet['id_str']
    user_id = tweet['user']['id_str']

    tx.run("""
    MERGE (t:Tweet {{
        id:{id},
        retweeted:{retweeted},
        quote_count:{quote_count},
        reply_count:{reply_count},
        retweet_count:{retweet_count}
    }})
    """.format(
        id=tweet_id,
        retweeted=tweet['retweeted'],
        quote_count=tweet['quote_count'],
        reply_count=tweet['reply_count'],
        retweet_count=tweet['retweet_count'],
    ))

    tx.run("""
    MERGE (u:User {{ id:{user} }})
    SET u.name='{name}', u.screen_name='{screen_name}', u.followers={followers}
    """.format(
        user=user_id,
        name=escape(tweet['user']['name']),
        screen_name=escape(tweet['user']['screen_name']),
        followers=tweet['user']['followers_count'],
    ))

    location = escape(tweet['user']['location'])\
        .lower()\
        .replace(',sverige', '').replace(', sverige', '')\
        .replace(',sweden', '').replace(', sweden', '')\
        .strip()

    tx.run("""
    MATCH (user:User {{ id:{user} }})
    MERGE (location:Location {{ name:'{location}' }})
    MERGE (user)-[:located]->(location)
    """.format(
        user=user_id,
        location=location
    ))

    hashtags = tweet['entities']['hashtags']
    for tag in hashtags:
        tx.run("""
        MATCH (t:Tweet {{ id:{tweet} }})
        MERGE (h:Hashtag {{ text:'{text}' }})
        MERGE (t)-[:has]->(h)
        """.format(
            tweet=tweet_id,
            text=escape(tag['text'])
        ))

    tx.run("""
    MATCH (t:Tweet {{ id:{tweet} }})
    MATCH (u:User {{ id:{user} }})
    MERGE (u)-[:tweets]->(t)
    """.format(
        tweet=tweet_id,
        user=user_id,
    ))

    if tweet['in_reply_to_status_id_str'] is not None:
        tx.run("""
        MATCH (tweet:Tweet {{ id:{tweet} }})
        MATCH (orig:Tweet  {{ id:{orig} }})
        MERGE (tweet)-[:retweet]->(orig)
        """.format(
            tweet=tweet_id,
            orig=tweet['in_reply_to_status_id_str']
        ))

    if tweet['in_reply_to_user_id_str'] is not None:
        tx.run("""
        MATCH (user:User {{ id:{user} }})
        MATCH (to:User   {{ id:{to} }})
        MERGE (user)-[:reply]->(to)
        """.format(
            user=user_id,
            to=tweet['in_reply_to_user_id_str']
        ))

    mentions = tweet['entities']['user_mentions']
    for mention in mentions:
        tx.run("""
        MATCH (user:User {{ id:{user} }})
        MATCH (other:User   {{ id:{other} }})
        MERGE (user)-[:mention]->(other)
        """.format(
            user=user_id,
            other=mention['id_str']
        ))


def escape(target):
    if target is None:
        return 'None'

    return target.replace('\\', '\\\\').replace('\'', '\\\'')


load()
driver.close()
