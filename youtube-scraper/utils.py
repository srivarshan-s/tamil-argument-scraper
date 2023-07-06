from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
from typing import Tuple


def get_api_key(file_path: str) -> str:
    with open(file_path, "r") as f:
        api_key: str = f.read()
    return api_key


def read_urls(file_path: str) -> Tuple[list[str], list[str]]:
    url_df: pd.DataFrame = pd.read_csv(file_path)
    url_df = url_df.drop_duplicates()
    urls: list[str] = list(url_df["Video.URL"])
    topics: list[str] = list(url_df["Topic"])
    return (urls, topics)


def process_text(text: str) -> str:
    text = text.replace("&#39;", "'")
    text = text.replace("&amp;", "&")
    text = text.replace("&quot;", '"')
    return text


def save_to_csv(dict_obj: dict, file_path: str) -> None:
    save_df: pd.DataFrame = pd.DataFrame(dict_obj)
    save_df = save_df.drop_duplicates()
    file_path_split: list[str] = file_path.split(".")
    file_path_raw: str = "".join(
        file_path_split[:-1]) + "_raw." + file_path_split[-1]
    save_df.to_csv(file_path_raw)
    save_df["Comment"] = save_df["Comment"].apply(process_text)
    file_path_processed: str = "".join(
        file_path_split[:-1]) + "_processed." + file_path_split[-1]
    save_df.to_csv(file_path_processed)


def get_video_comments(id: str, api_obj: build) -> list[str]:
    try:
        # Retrieve the video's comment threads
        comments: list[str] = []
        next_page_token = None

        while True:
            # Request the comment threads for the specified video
            response = api_obj.commentThreads().list(
                part='snippet',
                videoId=id,
                pageToken=next_page_token,
                # maxResults=100
            ).execute()

            # Extract the comments from the response
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)

            # Check if there are more comment threads to retrieve
            next_page_token = response.get('nextPageToken')

            if not next_page_token:
                break

        return comments

    except HttpError as e:
        print(f'An HTTP error {e.resp.status} occurred: {e.content}')
        return []
