import time

import pandas as pd

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

from utils import is_tamil


data=[]
video_list = [
        "https://www.youtube.com/watch?v=osnJ8vJ4xfc",
        # "https://www.youtube.com/watch?v=DK9sVSlDbKE",
        # "https://www.youtube.com/watch?v=17_xfg6BsB0",
        ]

driver = Chrome(service=Service(ChromeDriverManager().install()))
# driver = Chrome(executable_path="/usr/bin/chromedriver")
wait = WebDriverWait(driver,15)

for video in video_list:
    
    driver.get(video)

    for item in range(200): 
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
        time.sleep(2)

    for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content"))):
        
        text = comment.text
        # if is_tamil(text):
        #     data.append(text)
        data.append(text)

df = pd.DataFrame(data, columns=['comment'])

df.to_csv("comments.tsv", sep="\t")
