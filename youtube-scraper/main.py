from utils import get_api_key, get_video_comments, read_urls, save_to_csv
from googleapiclient.discovery import build


def main() -> None:
    # Get the API key
    API_KEY: str = get_api_key(file_path="api_key.txt")
    # Define the service
    API_SERVICE_NAME: str = "youtube"
    # Define the API version
    API_VERSION: str = "v3"

    # Initialize the YouTube API
    youtube: build = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)

    # Initialize list to store the URLs
    video_urls: list[str] = []
    # Initialize list to store the topics
    video_topics: list[str] = []
    # Read the URLs and topics from file
    video_urls, video_topics = read_urls(file_path="urls.csv")

    # Initialize a dictionary to save comments
    save_dict: dict = {}
    # Initialize list to store the URLs
    save_dict["Video.URL"]: list = []
    # Initialize list to store the topics
    save_dict["Topic"]: list = []
    # Initialize list to store the comments
    save_dict["Comment"]: list = []

    # Iterate over each URL
    for url, topic in zip(video_urls, video_topics):
        # Print the URL to console
        print("URL:", url)
        # Check if the URL is a short
        if "shorts" in url:
            # Get the short id from the URL
            video_id: str = url.split("/")[-1]
        # Check if the URL is a video
        elif "watch" in url:
            # Get the video id from the URL
            video_id: str = url.split("=")[-1]
        else:
            print("ERROR: url is neither a video nor a short!")
        # Get the list of comments for the video id
        comments: list[str] = get_video_comments(id=video_id, api_obj=youtube)
        # Add each comment and corresponding topic and URL to the dictionary
        for comment in comments:
            save_dict["Video.URL"].append(url)
            save_dict["Topic"].append(topic)
            save_dict["Comment"].append(comment)

    # Save the dictionary to a csv file
    save_to_csv(save_dict, "yt_comments.csv")


if __name__ == "__main__":
    main()
