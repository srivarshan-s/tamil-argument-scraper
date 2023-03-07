import pandas as pd
import numpy as np
import pycld2 as cld
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


def detect_lang(dataframe, column):

    lang_list = []
    texts = dataframe[column]

    for text in texts:
        # Remove @ mentions and urls
        text = re.sub(r"(?:\@|https?\://)\S+", "", text)
        _, _, _, lang = cld.detect(text,  returnVectors=True)
        lang = [ele[2] for ele in lang]
        # Check for english
        if len(lang) == 1 and lang[0] != "Unknown":
            lang_list.append(lang[0])
        else:
            lang_list.append("CODE-MIXED")

    dataframe["Language"] = lang_list

    return dataframe


if __name__ == "__main__":

    df = pd.read_csv("tweet_comments.csv")

    df = replace_tags(dataframe=df, 
            columns=["Replying to", "Tweet", "Parent Tweet"])

    df = detect_lang(dataframe=df, column="Tweet")
    
    print(df)
    df.to_csv("tweet_comments_processed.csv", index=False, encoding="utf-8")
