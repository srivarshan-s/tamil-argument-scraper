import time
import os

import pandas as pd

from utils import close_ntfn_popup

from selenium.webdriver import Chrome
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# from webdriver_manager.chrome import ChromeDriverManager


url_df = pd.read_csv("urls.csv")
urls = url_df["URL"]
topics = url_df["Topic"]
main_tweets = url_df["Tweet"]

tweets = []

for url, topic, main_tweet in zip(urls, topics, main_tweets):

    try:

        try:
            # driver = Chrome(service=Service(ChromeDriverManager().install()))
            driver = Chrome("./chromedriver")
            driver.maximize_window()
            driver.get(url)

        except:
            print(url, "not accessible!")
            continue

        time.sleep(10)

        close_ntfn_popup(driver, By)

        result = False
            
        # Get scroll height after first time page load
        last_height = driver.execute_script("return document.body.scrollHeight")

        last_elem=''
        current_elem=''

        scroll_height = 0

        while True:

            cmd = "window.scrollTo(0, " + str(scroll_height) + ");"
            driver.execute_script(cmd)
            scroll_height +=100

            last_height = driver.execute_script("return document.body.scrollHeight")
            if scroll_height + 200 > last_height:
                break

            # time.sleep(1)

            close_ntfn_popup(driver, By)

            #update all_tweets to keep loop
            all_tweets = driver.find_elements(By.XPATH, '//div[@data-testid]//article[@data-testid="tweet"]')

            for item in all_tweets:

                try:
                    date = item.find_element(By.XPATH, './/time').text
                except:
                    date = '[empty]'

                try:
                    text = item.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text
                except:
                    text = '[empty]'

                try:
                    replying_to = item.find_element(By.XPATH, './/div[contains(text(), "Replying to")]//a').text
                except:
                    replying_to = '[empty]'
                    continue
            
                #Append new tweets replies to tweet array
                if text == "" or text == "[empty]":
                    continue
                if " · " in date:
                    continue
                tweets.append([replying_to, text, date, topic, main_tweet])
                    
                if (last_elem == current_elem):
                    result = True
                else:
                    last_elem = current_elem

        driver.close()
        driver.quit()

    except:
        print(url, "not accessible!")
        print("Chrome driver crashed!")
        continue


if os.path.isfile("./tweet_comments.csv"):
    df = pd.read_csv("./tweet_comments.csv")
    df_new = pd.DataFrame(tweets, columns=["Replying to", "Tweet", "Date of Tweet", "Topic", "Parent Tweet"])
    df = pd.concat([df, df_new], ignore_index = True)
    df.reset_index()

else:
    df = pd.DataFrame(tweets, columns=["Replying to", "Tweet", "Date of Tweet", "Topic", "Parent Tweet"])
    
df = df.drop_duplicates()
df.to_csv("tweet_comments.csv", index=False, encoding="utf-8")
