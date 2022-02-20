import os

os.system("snscrape --jsonl --progress --max-results 10000 --since 2021-01-01 twitter-search \"vaccine\"> user-tweets.json")
