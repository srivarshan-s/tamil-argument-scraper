import pandas as pd
import numpy as np
import re


def replace_tags(dataframe, columns):

    user_tags = []
    mention_re = "(^|[^@\w])@(\w{1,15})"

    for col in columns:
        for ele in dataframe[col]:
            mentions = re.findall(mention_re, ele)
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

    for col in columns:
        new_list = list(dataframe[col])
        for tag, dummy in user_tag_dict.items():
            for idx in range(len(dataframe)):
                new_list[idx] = new_list[idx].replace(tag, dummy)
        dataframe[col] = new_list

    return dataframe


if __name__ == "__main__":

    df = pd.read_csv("tweet_comments.csv")

    df = replace_tags(dataframe=df, columns=["Replying to", "Tweet", "Parent Tweet"])
    
    print(df)
