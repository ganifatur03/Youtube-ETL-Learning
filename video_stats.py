from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()

my_yt_api = os.getenv("YOUTUBE_API")
channel_handle = "officialhigedandism"

url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={channel_handle}&key={my_yt_api}"

def get_playlist_id(your_url):
  try:
    response = requests.get(your_url)
    response.raise_for_status()  # Raise an error for bad responses

    data = response.json()
    print(json.dumps(data, indent=4))

    data_item = data["items"][0]
    playlist_id = data_item["contentDetails"]["relatedPlaylists"]["uploads"]
    return playlist_id
  
  except requests.exceptions.RequestException as e:
    raise e
  
if __name__ == "__main__":
    playlist_id = get_playlist_id(url)
    print(f"Playlist ID: {playlist_id}")