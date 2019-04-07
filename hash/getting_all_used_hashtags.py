import pymongo
from collections import Counter

# Reading in all tweets
f = open('tweets', 'r')
data = f.readlines()
f.close()


# Get all hashtags
tags = []
prefix = 'hashtags":[{"text":"'
for d in data:
    start = d.find(prefix)
    if start < 0:
        continue
    start += len(prefix)
    ending = d.find('],"urls":')
    wanted = d[start:ending]
    wanted = wanted.split("},{")

    for element in wanted:
        start = element.find('"text":"')
        ending2 = element.find('","')
        if start < 0:
            tags.append(element[0:ending2])
        else:
            tags.append(element[start:ending2])

# Some fixing because of above code...
tags2 = []
for tt in tags:
    if tt.find('"text":"') == -1:
        tags2.append(tt)
    else:
        tags2.append(tt[8:])

# Sorting and making data usable
uniq = []
tags2 = filter(None, tags2)
a = dict(Counter(tags2))
a_sorted = sorted(a.items(), key=lambda kv: kv[1])
a_sorted.reverse()