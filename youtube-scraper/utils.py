from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
from typing import Tuple


# Function to get the API key from a text file
def get_api_key(file_path: str) -> str:
    # Open the text file
    with open(file_path, "r") as f:
        # Read the key
        api_key: str = f.read()
    # Return the API key
    return api_key


# Function to read the URLs and topics from a csv file
def read_urls(file_path: str) -> Tuple[list[str], list[str]]:
    # Read the csv file as a pandas DataFrame
    url_df: pd.DataFrame = pd.read_csv(file_path)
    # Drop the duplicate entries in the DataFrame
    url_df = url_df.drop_duplicates()
    # Get the URLs as a list
    urls: list[str] = list(url_df["Video.URL"])
    # Get the topics as a list
    topics: list[str] = list(url_df["Topic"])
    # Return the URLs and the topics
    return (urls, topics)


# Function to process the raw text
def process_text(text: str) -> str:
    # Replace symbol representations with the actual symbols
    text = text.replace("&#39;", "'")
    text = text.replace("&amp;", "&")
    text = text.replace("&quot;", '"')
    return text


# Function to save the dictionary with comments collected to a csv file
def save_to_csv(dict_obj: dict, file_path: str) -> None:
    # Create a pandas DataFrame from the dictionary
    save_df: pd.DataFrame = pd.DataFrame(dict_obj)
    # Drop the duplicate entries in the DataFrame
    save_df = save_df.drop_duplicates()
    # Split the file path into file name and file extension
    file_path_split: list[str] = file_path.split(".")
    # Add _raw to the file name
    file_path_raw: str = "".join(
        file_path_split[:-1]) + "_raw." + file_path_split[-1]
    # Save the raw comments
    save_df.to_csv(file_path_raw)
    # Process the comments
    save_df["Comment"] = save_df["Comment"].apply(process_text)
    # Add _processed to the file name
    file_path_processed: str = "".join(
        file_path_split[:-1]) + "_processed." + file_path_split[-1]
    # Save the processed comments
    save_df.to_csv(file_path_processed)


# Function to get the video comments from the video id
def get_video_comments(id: str, api_obj: build) -> list[str]:
    try:
        # Initialize list to store the comments
        comments: list[str] = []
        # Initialize variable to check for next page of comments
        next_page_token: str | None = None

        # Loop until there are no more comments found
        while True:
            # Request the comment threads for the specified video
            response: dict = api_obj.commentThreads().list(
                part='snippet',
                videoId=id,
                pageToken=next_page_token,
                # maxResults=100
            ).execute()

            # Iterate over each element in the response
            for item in response['items']:
                # Extract the top level comment
                topLevelComment: dict = item['snippet']['topLevelComment']
                # Extract the comment's text
                comment: str = topLevelComment['snippet']['textDisplay']
                # Add the comment text to the list of comments
                comments.append(comment)

            # Check if there are more comment threads to retrieve
            next_page_token = response.get('nextPageToken')

            # If there are no more comments, exit the loop
            if not next_page_token:
                break

        # Return the list of comments
        return comments

    # Handle error
    except HttpError as e:
        # Print the error to console
        print(f'An HTTP error {e.resp.status} occurred: {e.content}')
        # Return empty list of comments
        return []
