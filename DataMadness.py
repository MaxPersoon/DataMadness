	
import pandas as pd

# Merge all files into one DataFrame
def dataMergeClean():

	
	hashtags = ["#vaccineskill", "#vaccinesharm", "#nojab", "#stoptheshot", "#VAIDS"]
	
	tweets = pd.read_json(f"data\\{hashtags[0]}-tweets.json", lines = True)
	
	for hashtag in hashtags[1:]:
	    tmp_df = pd.read_json(f"data\\{hashtag}-tweets.json", lines = True)
	    tweets = pd.concat([tweets, tmp_df])
	
	tweets
	
	
	# In[771]:
	
	
	tweets.shape
	
	
	# In[772]:
	
	
	tweets.columns.values
	
	
	# In[773]:
	
	
	# Drop columns that contain useless information
	columns_to_drop = ['_type', 'url', 'renderedContent', 'conversationId', 'source', 'sourceUrl', 'tcooutlinks', 'coordinates', 'cashtags']
	tweets = tweets.drop(columns=columns_to_drop)
	tweets
	
	
	# In[774]:
	
	
	tweets['id'].nunique()
	
	
	# In[775]:
	
	
	# Number of unique Tweets != total number of Tweets --> duplicate entries
	# Drop duplicate Tweets
	tweets = tweets.drop_duplicates(subset='id')
	
	# Use Tweet ID to identify data entries
	tweets['id'] = tweets['id'].map(str)
	tweets = tweets.set_index('id')
	
	# The "+00:00" in entries in the 'date' column indicate the UTC timezone. It looks ugly, so let's remove it.
	tweets['date'] = tweets['date'].dt.tz_localize(None)
	
	tweets
	
	
	# In[776]:
	
	
	tweets['lang'].unique()
	
	
	# In[777]:
	
	
	# Clean up 'lang' column
	replacements = {
	    'en': 'English',
	    'und': 'Unknown',
	    'fr': 'French',
	    'es': 'Spanish',
	    'pl': 'Polish',
	    'zh': 'Chinese',
	    'tr': 'Turkish',
	    'nl': 'Dutch',
	    'ca': 'Catalan',
	    'it': 'Italian',
	    'ar': 'Arabic',
	    'el': 'Greek',
	    'cs': 'Czech',
	    'sv': 'Swedish',
	    'de': 'German',
	    'hi': 'Hindi',
	    'pt': 'Portugese',
	    'da': 'Danish',
	    'tl': 'Tagalog',
	    'sr': 'Serbian',
	    'in': 'Unknown',
	    'et': 'Estonian',
	    'no': 'Norwegian',
	    'lv': 'Latvian',
	    'ht': 'Haitian',
	    'ja': 'Japanese',
	    'ro': 'Romanian',
	    'fi': 'Finnish',
	    'cy': 'Welsch',
	    'lt': 'Lithuanian',
	    'sl': 'Slovenian',
	    'is': 'Icelandic',
	    'th': 'Thai',
	    'hu': 'Hungarian',
	    'mr': 'Marathi',
	    'bg': 'Bulgarian',
	    'ko': 'Korean',
	}
	# Symbolic meanings gathered from https://developer.twitter.com/en/docs/twitter-for-websites/supported-languages and https://www.loc.gov/standards/iso639-2/php/code_list.php
	tweets['lang'] = tweets['lang'].replace(replacements)
	tweets
	
	
	# In[778]:
	
	
	users = tweets['user'].tolist()
	users = pd.DataFrame(users)
	users
	
	
	# In[779]:
	
	
	# Drop columns that contain useless information
	columns_to_drop = ['_type', 'displayname', 'rawDescription', 'linkTcourl', 'profileImageUrl', 'profileBannerUrl', 'label', 'url']
	users = users.drop(columns=columns_to_drop)
	
	# Replace 'user' column in Tweets with userIds
	users['id'] = users['id'].map(str)
	tweets['user'] = users['id'].values
	tweets = tweets.rename(columns={'user': 'userId'})
	
	# Drop duplicate users
	users = users.drop_duplicates(subset='id')
	
	# Use user ID to identify data entries
	users = users.set_index('id')
	
	# The "+00:00" in entries in the 'created' column indicate the UTC timezone. It looks ugly, so let's remove it.
	users['created'] = pd.to_datetime(users['created'])
	users['created'] = users['created'].dt.tz_localize(None)
	
	# Fix column 'descriptionUrls'
	replacement = []
	
	for entry in users['descriptionUrls']:
	    urls = 'None'
	    if entry is not None:
	        urls = []
	        for url in entry:
	            urls.append(url['url'])
	    replacement.append(urls)
	
	users['descriptionUrls'] = replacement
	
	users
	
	
	# In[780]:
	
	
	tweets
	
	
	# In[781]:
	
	
	# Fix column 'outlinks'
	replacement = []
	
	for outlink in tweets['outlinks']:
	    link = 'None'
	    if outlink is not None:
	        link = outlink[0]
	    replacement.append(link)
	
	tweets['outlinks'] = replacement
	
	
	# In[782]:
	
	
	tweets['retweetedTweet'].unique()
	
	
	# In[783]:
	
	
	# Column 'retweetedTweet' is useless --> drop it
	tweets = tweets.drop(columns='retweetedTweet')
	
	# Fix column 'media'
	replacement = []
	
	for entry in tweets['media']:
	    containsMedia = False
	    if entry is not None:
	        containsMedia = True
	    replacement.append(containsMedia)
	
	tweets['media'] = replacement
	tweets = tweets.rename(columns={'media': 'containsMedia'})
	
	# Fix column 'quotedTweet'
	replacement = []
	for entry in tweets['quotedTweet']:
	    quoteTweetID = 'None'
	    if entry is not None:
	        quoteTweetID = str(entry['id'])
	    replacement.append(quoteTweetID)
	
	tweets['quotedTweet'] = replacement
	tweets = tweets.rename(columns={'quotedTweet': 'quoteTweetId'})
	
	# Fix column 'inReplyToTweetId'
	tweets['inReplyToTweetId'] = tweets['inReplyToTweetId'].fillna(0)
	tweets['inReplyToTweetId'] = tweets['inReplyToTweetId'].map(int).map(str)
	tweets['inReplyToTweetId'] = tweets['inReplyToTweetId'].replace({'0': 'None'})
	
	# Fix column 'inReplyToUser'
	replacement = []
	
	for entry in tweets['inReplyToUser']:
	    replyUserId = 'None'
	    if entry is not None:
	        replyUserId = str(entry['id'])
	    replacement.append(replyUserId)
	
	tweets['inReplyToUser'] = replacement
	tweets = tweets.rename(columns={'inReplyToUser': 'inReplyToUserId'})
	
	# Fix column 'place'
	replacement = []
	
	for entry in tweets['place']:
	    country = 'None'
	    if entry is not None:
	        country = entry['country']
	    replacement.append(country)
	
	tweets['place'] = replacement
	tweets = tweets.rename(columns={'place': 'country'})
	
	# Fix column 'mentionedUsers'
	replacement = []
	
	for entry in tweets['mentionedUsers']:
	    mentionedUserIds = 'None'
	    if entry is not None:
	        mentionedUserIds = []
	        for mentionedUser in entry:
	            mentionedUserId = str(mentionedUser['id'])
	            mentionedUserIds.append(mentionedUserId)
	    replacement.append(mentionedUserIds)
	
	tweets['mentionedUsers'] = replacement
	tweets = tweets.rename(columns={'mentionedUsers': 'mentionedUserIds'})
	
	tweets
	
	return users

	