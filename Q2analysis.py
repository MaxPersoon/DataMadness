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
    print("what the actual yeeticus")

userDict={}

