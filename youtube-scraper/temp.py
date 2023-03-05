import pandas as pd
import pycld2 as cld2

df = pd.read_csv("./comments.csv")
comments = df["comment"]

for comment in comments:
    if type(comment) == str:
        _, _, _, lang = cld2.detect(comment,  returnVectors=True)
        if len(lang) == 1 and lang[0][2] == "TAMIL":
            print(comment)