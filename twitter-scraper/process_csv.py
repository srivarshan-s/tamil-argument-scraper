import pandas as pd
import numpy as np
import re


if __name__ == "__main__":

    df = pd.read_csv("tweet_comments.csv")

    user_tags = list(df["Replying to"]) 

    mention_re = "(^|[^@\w])@(\w{1,15})"

    for tweet in df["Tweet"]:
        mentions = re.findall(mention_re, tweet)
        for _, tag in mentions:
            tag = '@' + tag
            user_tags.append(tag)

    user_tags = np.unique(user_tags)

    dummy_tags = []
    for idx, tag in enumerate(user_tags):
        dummy_tags.append("@USER_" + str(idx+1))

    user_tag_dict = {}
    for tag, dummy in zip(user_tags, dummy_tags):
        user_tag_dict[tag] = dummy

    new_tweets = list(df["Tweet"])
    for idx in range(len(new_tweets)):
        for tag, dummy in user_tag_dict.items():
            new_tweets[idx] = new_tweets[idx].replace(tag, dummy)

    print(new_tweets)
