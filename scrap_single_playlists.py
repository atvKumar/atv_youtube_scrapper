import os
import json
import slugify
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from private_playlists import blacklisted

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
# client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"
DEVELOPER_KEY = "" # Enter your key here

youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

with open("All_Playlists.json", encoding="utf-8") as json_file:
    data = json.load(json_file)

# for item in data["items"]:
#     print(item['id'], "\n", item['snippet']['title'], "\n", item['snippet']['description'], "\n", item['snippet']['thumbnails']['high']['url'], "\n\n\n")
no = 1
for item in data["items"]:
    slug_filename = slugify.slugify(item['snippet']['title'])
    
    request = youtube.playlistItems().list(
        part="snippet,contentDetails, status",
        playlistId=f"{item['id']}",
        maxResults=50,
        prettyPrint=False
    )
    response = request.execute()
    # json_object = json.dumps(response, ensure_ascii=False, indent = 4) 
    if f"{slug_filename}.json" not in blacklisted:
        print(no,"|" ,f"{slug_filename}.json")
        with open(f"sub_playlist\\{slug_filename}.json", "w", encoding="utf-8") as outfile:
            json.dump(response, outfile, ensure_ascii=False)
        no += 1
    # if os.path.exists(f"sub_playlist\\{slug_filename}.json"):
    #     print(">>>>>>>>>>>>>>>>>>>>", f"sub_playlist\\{slug_filename}_1.json")
    #     with open(f"sub_playlist\\{slug_filename}_1.json", "w", encoding="utf-8") as outfile:
    #             json.dump(response, outfile, ensure_ascii=False)
    # else:
    #     with open(f"sub_playlist\\{slug_filename}.json", "w", encoding="utf-8") as outfile:
    #                     json.dump(response, outfile, ensure_ascii=False)
