import os
import pickle
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

if os.path.isfile("usersFile.pickle"):
    usersFile = open('usersFile.pickle', 'rb')
    users = pickle.load(usersFile)
else:
    users = {}
    print("yo wtf")

userDict={}

# def addUserToDict(user):
#     userDict[str(user.entity.id)] = user
#
# with ThreadPoolExecutor(max_workers=50) as pool:
#     response_list = list(tqdm(pool.map(addUserToDict, users)))

for user in users:
    try:
        userDict[str(user.id)]=user
    except Exception as e:
        print(e)

print(userDict.keys())