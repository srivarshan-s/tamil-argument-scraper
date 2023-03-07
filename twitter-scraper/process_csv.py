import pandas as pd
import numpy as np
import re


if __name__ == "__main__":

    df = pd.read_csv("tweet_comments.csv")
    # print(df.head())

    user_tags = list(df["Replying to"]) 
    # print(user_tags)

    mention_re = "(^|[^@\w])@(\w{1,15})"

    for tweet in df["Tweet"]:
        mentions = re.findall(mention_re, tweet)
        for _, tag in mentions:
            tag = '@' + tag
            user_tags.append(tag)

    user_tags = np.unique(user_tags)
    # print(user_tags)

    dummy_tags = []
    for idx, tag in enumerate(user_tags):
        dummy_tags.append("@USER_" + str(idx+1))

    # print(dummy_tags)

    user_tag_dict = {}
    for tag, dummy in zip(user_tags, dummy_tags):
        user_tag_dict[tag] = dummy

    print(user_tag_dict)
