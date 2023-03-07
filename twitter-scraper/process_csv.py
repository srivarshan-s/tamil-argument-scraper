import pandas as pd
import numpy as np

df = pd.read_csv("tweet_comments.csv")
# print(df.head())

user_tags = np.unique(df["Replying to"]) 
# print(user_tags)

for tweet in df["Tweet"]:
    print(tweet)
