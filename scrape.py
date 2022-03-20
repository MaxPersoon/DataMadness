import os

hashtags = ["#vaccineskill", "#vaccinesharm", "#nojab", "#stoptheshot", "#VAIDS"]

for hashtag in hashtags:
    print(f"Now scraping for {hashtag}")
    os.system(f"snscrape --jsonl --progress --max-results 50000 --since 2020-01-01 twitter-search \"{hashtag} until"
              f":2022-02-21\" > {hashtag}-tweets.json")
