from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()

YT_API = os.getenv("YOUTUBE_API")
channel_handle = "officialhigedandism"
maxResult = 50
video_id_limit = 60

def get_playlist_id():
  url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={channel_handle}&key={YT_API}"

  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses

    data = response.json()
    # print(json.dumps(data, indent=4))

    data_item = data["items"][0]
    playlist_id = data_item["contentDetails"]["relatedPlaylists"]["uploads"]
    return playlist_id
  
  except requests.exceptions.RequestException as e:
    raise e
  
def get_video_ids(playlist_id):
  list_video_ids = []
  pageToken = None
  base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResult}&playlistId={playlist_id}&key={YT_API}"

  try:
      
      while True:
        url = base_url

        if pageToken:
          url += f"&pageToken={pageToken}"

        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()

        for item in data.get("items", []):
          video_id = item['contentDetails']['videoId']
          list_video_ids.append(video_id)
          if video_id_limit is not None and len(list_video_ids) >= video_id_limit:
              return list_video_ids

        pageToken = data.get("nextPageToken")

        if not pageToken:
          break

      return list_video_ids

  except requests.exceptions.RequestException as e:
    raise e
  
if __name__ == "__main__":
    playlist_id = get_playlist_id()
    print(f"Playlist ID: {playlist_id}")
    video_ids = get_video_ids(playlist_id)
    print(f"\nVideo IDs: {video_ids}")