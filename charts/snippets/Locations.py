from collections import Counter
import numpy as np
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.cbook as cbook
diabetes_tweets = open("diabetes_tweets.json", "r", encoding="utf8")
locations = []
number_of_location_tweets = []


for line in diabetes_tweets:
    elements = line.split(",")
    for element in elements:
        if element.startswith('"full_name'):
            if elements[elements.index(element)+1] == " Sweden\"":
                locations.append(element.split(':')[1] + ", Sverige\"")
            else:
                locations.append(element.split(':')[1] + "," + elements[elements.index(element) + 1])
print(locations)
a = dict(Counter(locations))
print(a)

locations = list(a.keys())
number_of_location_tweets = list(a.values())

print(number_of_location_tweets)
print(locations)

locations_over_five_tweets = []
for location in locations:
    if number_of_location_tweets[locations.index(location)] > 5:
        locations_over_five_tweets.append(location)

number_of_location_tweets_over_5 = []
for number in number_of_location_tweets:
    if number > 5:
        number_of_location_tweets_over_5.append(number)
print(number_of_location_tweets_over_5)
print(locations_over_five_tweets)
map_of_sweden = cbook.get_sample_data('mapofsweden.jpg', 0)
img = plt.imread(map_of_sweden)
fig, ax = plt.subplots(1)
ax.set_aspect('equal')
ax.imshow(img)

for location in locations_over_five_tweets:
    if locations_over_five_tweets.index(location) == 0:
        x = 78
        y = 720
        circle = Circle((x, y), number_of_location_tweets_over_5[0] * 0.4)
        circle.set_edgecolor("black")
        ax.add_patch(circle)
    elif locations_over_five_tweets.index(location) == 1:
        x = 230
        y = 530
        circle = Circle((x, y), number_of_location_tweets_over_5[1] * 0.4)
        circle.set_edgecolor("black")
        ax.add_patch(circle)
    elif locations_over_five_tweets.index(location) == 2:
        x = 220
        y = 500
        circle = Circle((x, y), number_of_location_tweets_over_5[2] * 0.4)
        circle.set_edgecolor("black")
        ax.add_patch(circle)
    elif locations_over_five_tweets.index(location) == 3:
        x = 235
        y = 610
        circle = Circle((x, y), number_of_location_tweets_over_5[3] * 0.4)
        circle.set_edgecolor("black")
        ax.add_patch(circle)
    elif locations_over_five_tweets.index(location) == 4:
        x = 44
        y = 608
        circle = Circle((x, y), number_of_location_tweets_over_5[4] * 0.4)
        circle.set_edgecolor("black")
        ax.add_patch(circle)
    elif locations_over_five_tweets.index(location) == 5:
        x = 290
        y = 190
        circle = Circle((x, y), number_of_location_tweets_over_5[5] * 0.4)
        circle.set_edgecolor("black")
        ax.add_patch(circle)
    elif locations_over_five_tweets.index(location) == 6:
        x = 190
        y = 520
        circle = Circle((x, y), number_of_location_tweets_over_5[6] * 0.4)
        circle.set_edgecolor("black")
        ax.add_patch(circle)
    elif locations_over_five_tweets.index(location) == 7:
        x = 40
        y = 570
        circle = Circle((x, y), number_of_location_tweets_over_5[7] * 0.4)
        circle.set_edgecolor("black")
        ax.add_patch(circle)
    elif locations_over_five_tweets.index(location) == 8:
        x = 220
        y = 520
        circle = Circle((x, y), number_of_location_tweets_over_5[8] * 0.4)
        circle.set_edgecolor("black")
        ax.add_patch(circle)
    elif locations_over_five_tweets.index(location) == 9:
        x = 135
        y = 530
        circle = Circle((x, y), number_of_location_tweets_over_5[9] * 0.4)
        circle.set_edgecolor("black")
        ax.add_patch(circle)
    elif locations_over_five_tweets.index(location) == 10:
        x = 50
        y = 615
        circle = Circle((x, y), number_of_location_tweets_over_5[10] * 0.4)
        circle.set_edgecolor("black")
        ax.add_patch(circle)
plt.show()
