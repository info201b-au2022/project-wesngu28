# Import Pandas for dataframe conversion and snscrape to scrape twitter.
# Re to clean tweets using regex

import pandas as pd
import snscrape.modules.twitter as sntwitter
import re

# Only get English Tweets

query = "lang:en"

# Initialize an empty array to store the tweets inside

tweets = []

# Get 3500 tweets. This is equal to around train + test set. I am doing 5 times the reddit test set
# because in some tests I did a lot of them are neutral which are kind of useless.

limit = 3500

# Iterate through the iterable generated by TwitterSearchScraper get_items call

for tweet in sntwitter.TwitterSearchScraper(query).get_items():

  # If we hit the max limit defined for the array, stop getting tweets

  if len(tweets) == limit:
    break

  # Append the tweets
  # I think we only need the content, but I think I'll get date, username, id , and url

  tweets.append([tweet.date, tweet.content, tweet.user.username, tweet.id, tweet.url])

# Create a dataframe from the array

tweets_df = pd.DataFrame(tweets, columns=['Date', 'Tweet', 'User', 'Tweet ID', 'Tweet Url'])

# Remove @, #, RT, links, and new line escape character. Done using regex substitution.
# These do not add anything to polarity and sentiment and could confuse the algorithm.

def cleanTweets(tweet):
  tweet = re.sub('@[A-Za-z0-9_]+', '', tweet)
  tweet = re.sub('#', '', tweet)
  tweet = re.sub('RT[\s]+', '', tweet)
  tweet = re.sub('https?:\/\/\S+', '', tweet)
  tweet = re.sub('\n', ' ', tweet)
  return tweet

# Apply cleanTweets to every single item in the tweets column

tweets_df['Cleaned Tweets'] = tweets_df['Tweets'].apply(cleanTweets)

# Save this dataframe

tweets_df.to_csv('Tweets 11-10-2022.csv', index=False)