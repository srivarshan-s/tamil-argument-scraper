from utils import get_api_key, get_video_comments, read_urls, save_to_csv
from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs

def main() -> None:
    API_KEY: str = get_api_key(file_path="api_key.txt")
    API_SERVICE_NAME: str = "youtube"
    API_VERSION: str = "v3"

    youtube: build = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)

    video_urls: list[str] = []
    video_topics: list[str] = []
    video_urls, video_topics = read_urls(file_path="urls.csv")

    save_dict: dict = {}
    save_dict["Video.URL"]: list = []
    save_dict["Topic"]: list = []
    save_dict["Comment"]: list = []
    
    for url, topic in zip(video_urls, video_topics):
        video_id: str = parse_qs(urlparse(url).query)['v'][0]
        print("URL:", url)
        comments: list[str] = get_video_comments(id=video_id, api_obj=youtube)
        for comment in comments:
            save_dict["Video.URL"].append(url)
            save_dict["Topic"].append(topic)
            save_dict["Comment"].append(comment)

    save_to_csv(save_dict, "yt_comments.csv")

if __name__ == "__main__":
    main()