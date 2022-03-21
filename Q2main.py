import pickle

import pandas as pd
import os
from snscrape.modules.twitter import TwitterUserScraper
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# if os.path.isfile("usersFile.pickle"):
#     usersFile = open('usersFile.pickle', 'rb')
#     users = pickle.load(usersFile)
# else:
#     users = {}

refresh = False  # reload Max's .jpynb as a script

if refresh:
    os.system("jupyter nbconvert --to script DataMadness.ipynb")
    f = open("DataMadness.py", "r")
    content = f.read().split("\n")
    content = content[5:]

    content.insert(4, "def dataMergeClean():\n")
    content.insert(-1, "return tweets\n")

    for i, x in enumerate(content):
        if i > 4: content[i] = "\t" + x

    f = open("DataMadness.py", "w")
    f.write("\t" + ("\n".join(content)))
    f.close()

from DataMadness import dataMergeClean

data = pd.DataFrame(dataMergeClean())

# print(data.columns.values)

users = []


def getUser(user):
    user=None
    try:
        user =TwitterUserScraper(str(user), isUserId=True).entity
    except Exception as e:
        user=None
    return user


users = data["userId"]

print("test")
with ThreadPoolExecutor(max_workers=20) as pool:
    response_list = list(tqdm(pool.map(getUser, users)))

print(response_list[:5])

usersFile = open('usersFile.pickle', 'wb')
pickle.dump(response_list, usersFile)
