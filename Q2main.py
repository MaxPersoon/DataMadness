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
    content.insert(-1, "return users\n")

    for i, x in enumerate(content):
        if i > 4: content[i] = "\t" + x

    f = open("DataMadness.py", "w")
    f.write("\t" + ("\n".join(content)))
    f.close()

from DataMadness import dataMergeClean

users = pd.DataFrame(dataMergeClean())

# print(data.columns.values)

usersFile = open('usersFile.pickle', 'wb')
pickle.dump(users, usersFile)
