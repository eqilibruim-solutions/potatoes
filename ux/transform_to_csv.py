import csv
import json


def yield_file():
    with open('./diabetes_tweets.json') as file:
        for record in file:
            yield record


fieldnames = ['id', 'text', 'location', 'created_at']
writer = csv.DictWriter(open('tweets.csv', 'w'), fieldnames=fieldnames, dialect='excel')
writer.writeheader()

for line in yield_file():
    tweet = json.loads(line)
    writer.writerow({
        'id': tweet['id'],
        'text': tweet['text'].replace('\n', '\\n'),
        'location': tweet['user']['location'],
        'created_at': tweet['created_at'],
    })
