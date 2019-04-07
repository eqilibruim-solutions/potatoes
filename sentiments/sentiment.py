import pandas as pd
import re
import string


# Import Tweet Data
tweets = pd.read_csv('tweets.csv', sep=',', names=["Id", "Text", "Location", "DateTime"])
tweets.head()


# Import Sentiment Data
sentiment = pd.read_csv('SentimentLexicon.csv', delimiter=",")
sentiment.head()


# Sentiment arrays
word = sentiment.as_matrix(columns=sentiment.columns[:1])
str = sentiment.as_matrix(columns=sentiment.columns[2:3])


# Tweet arrays
tweet_id = tweets.as_matrix(columns=tweets.columns[:1])
texts = tweets.as_matrix(columns=tweets.columns[1:2])

# Flattening the list
word_list = word.tolist()
word2 = []
for w in word_list:
    for x in w:
        word2.append(x)

# Aweful thing to check every word in each tweet
# and give it a sentiment score.
sentiment = []
id_index = 0
word_str = 0
for t in texts:
    t_words = re.sub('[' + string.punctuation + ']', '', t[0]).split()
    score = 0
    # t_words = re.findall(r'\w+', t)
    w_index = 0
    for w in t_words:
        # Sentiment check each word
        if w in word2:
            index = word2.index(w)
            word_str = str[index][0]
            score += word_str

            # Some minor improvement
            prev_word = t_words[w_index]
            if prev_word == "lite":
                if word_str > 0:
                    score -= 1
                else:
                    score += 1
            elif prev_word == "mycket":
                if word_str > 0:
                    score += 1
                else:
                    score -= 1
            elif prev_word == "värdelös" or prev_word == "enastående":
                if word_str > 0:
                    score += 2
                else:
                    score -= 2
        w_index += 1

    tmp = (tweet_id[id_index][0], score)
    sentiment.append(tmp)
    id_index += 1;


# Print to File
f = open('sentiment_score.txt', 'w')
f.write("[")
for arr in sentiment:
    f.write(arr.__str__() + ",")
f.write("]")
f.close()