import math
import numpy as np
import pandas as pd
import pycountry
import seaborn as sns
from matplotlib import pyplot as plt

from DataMadness import dataMergeClean
from DataMadness2 import dataMergeClean2




users = dataMergeClean()
usersCovid = dataMergeClean2("COVID19")

users=pd.DataFrame(users)
usersCovid=pd.DataFrame(usersCovid)

print(users.shape)

users.columns.values[6] = "followingCount"

print(users.shape)

print(users.columns.values)

sns.histplot(users["created"], bins=100)
plt.title("Distribution of Account Creation Year Over the covid hashtags Dataset")
plt.xlabel("Year")
# plt.xlim(date(2008,1,1),date(2010, 1, 1))
plt.ylabel("Accounts Created")

# plt.show()

# users = users[users["followersCount"] < 40000]  # remove 9 outliers

print("followersCount description")
print(users["followersCount"].describe())

sns.histplot(users["followersCount"], bins=1000)
plt.title("Followers count for the covid hashtags dataset")
plt.xlabel("Followers")
plt.ylabel("Frequency")
plt.xscale('log')
plt.axvline(x=users["followersCount"].median(), color='blue', ls='--', lw=2.5)
plt.axvline(x=users["followersCount"].mean(), color='red', lw=2.5)
# plt.show()

# users = users[users["statusesCount"] < 40000]  # remove outliers
print("statusesCount description")
print(users["statusesCount"].describe())

sns.histplot(users["statusesCount"], bins=1000)
plt.title("Statuses count for the covid hashtags dataset")
plt.xlabel("Statuses")
# plt.xlim(0,5000)
plt.xscale('log')
plt.ylabel("Frequency")
plt.axvline(x=users["statusesCount"].median(), color='blue', ls='--', lw=2.5)
plt.axvline(x=users["statusesCount"].mean(), color='red', lw=2.5)
plt.show()


# the code for the location graph takes a long time

# def parseLocation(location):
#     country = location
#     if "united states" in location.lower or location.lower=="usa" or location.lower=="us":
#         return "United States"
#     if location != "":
#         try:
#             place = location.split(",")[-1]
#             country = pycountry.countries.search_fuzzy(place)[0].name
#         except:
#             country = location
#     return country
#
#
# usersCovid['location'] = usersCovid['location'].apply(parseLocation)
#
# locations = usersCovid["location"].value_counts()[1:10]
#
# ax = sns.barplot(y=locations.index, x=locations.values)
# plt.title("Twitter users locations for #covid19 tweets")
# plt.tight_layout(pad=1)
# plt.show()

users["followersCount"] = users["followersCount"].apply(lambda x: math.log10(x + 1))
usersCovid["followersCount"] = usersCovid["followersCount"].apply(lambda x: math.log10(x + 1))

print(users["followersCount"])

antivaxFollowersCount = pd.DataFrame(users["followersCount"].rename("antivaxFollowersCount")).reset_index(drop=True)
covidFollowersCount = pd.DataFrame(usersCovid["followersCount"].rename("covidFollowersCount")).reset_index(drop=True)
antivaxFollowersCount = antivaxFollowersCount.join(covidFollowersCount, how="outer")

ax = sns.violinplot(data=antivaxFollowersCount, showmedians=True)

# ax = sns.boxplot(data=covidFollowersCount)
# plt.yscale('symlog')
plt.yticks(np.arange(0, 8), [format(x, '.0E') for x in 10 ** np.arange(0, 8)])
ax.set_ylim(bottom=0)
plt.title('Comparison between followers in antivax tweets and #COVID19 tweets')
plt.show()

antivaxRegistrationDate = pd.DataFrame(
    users["created"].apply(lambda x: int(x.strftime('%Y'))).rename("antivaxCreated")).reset_index(drop=True)
covidRegistrationDate = pd.DataFrame(
    usersCovid["created"].apply(lambda x: int(x.strftime('%Y'))).rename("covidCreated")).reset_index(drop=True)
comparisonRegistrationDate = antivaxRegistrationDate.join(covidRegistrationDate, how="outer")

print(comparisonRegistrationDate)

ax = sns.violinplot(data=comparisonRegistrationDate, showmedians=True)
plt.yticks(np.arange(2005, 2023))

# ax = sns.boxplot(data=covidFollowersCount)
plt.title('User registration dates in antivax tweets vs #COVID19 tweets')
plt.show()

users["statusesCount"] = users["statusesCount"].apply(lambda x: math.log10(x + 1))
usersCovid["statusesCount"] = usersCovid["statusesCount"].apply(lambda x: math.log10(x + 1))

print(users["statusesCount"])

antivaxStatusesCount = pd.DataFrame(users["statusesCount"].rename("antivaxStatusesCount")).reset_index(drop=True)
covidStatusesCount = pd.DataFrame(usersCovid["statusesCount"].rename("covidStatusesCount")).reset_index(drop=True)
antivaxStatusesCount = antivaxStatusesCount.join(covidStatusesCount, how="outer")

ax = sns.violinplot(data=antivaxStatusesCount, showmedians=True)

# ax = sns.boxplot(data=covidStatusesCount)
# plt.yscale('symlog')
plt.yticks(np.arange(0, 8), [format(x, '.0E') for x in 10 ** np.arange(0, 8)])
ax.set_ylim(bottom=0)
plt.title('User statuses posted antivax tweets vs #COVID19 tweets')
plt.show()
