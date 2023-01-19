# -----------------------------------------------------------------------------
# Generate Video Data Fixture to be imported into Django vod_backend APP
# -----------------------------------------------------------------------------
import json
from os.path import exists
# Load the extracted and prepared data from extract_playlist_data.py
with open("thisone.json", encoding="utf-8") as json_file:
    data = json.load(json_file)

result = []
rest = []
for index, playlist in enumerate(data, 1):
    x = [video for video in data[playlist]["items"]]    
    for i in x:
        item = data[playlist]["items"][i]['Name']
        if item not in result:
            result.append(item)
            rest.append(data[playlist]["items"][i])
        # else:
        #     print(item, "<<<<<<<<<<<<<<<<<<<")
image_files = []
print(len(rest))
videos = []
for x, a in enumerate(rest, 1):
    # print(x, a)
    # break
    video_item = {"model": "vod.video", "pk": x}
    video_field_data = {}
    video_field_data["title"] = a["Name"]
    video_field_data["slug"] = a["slug"]
    video_field_data["type_id"] = 1
    video_field_data["language_id"] = a["language"]
    video_field_data["description"] = a["description"]
    video_field_data["external_url"] = a["url"]
    video_field_data["date_uploaded"] = a["date_uploaded"].replace('+00:00', 'Z')
    video_field_data["view_count"] = 0
    video_field_data["poster_image"] = f"video_thumbnail/{a['slug']}.jpg"
    video_field_data["status"] = "Public"
    video_field_data["post_activation"] = False
    video_field_data["activation_date"] = None
    video_item["fields"] = video_field_data
    videos.append(video_item)

    if video_field_data["poster_image"] not in image_files:
        image_files.append(f"video_thumbnail/{a['slug']}.jpg")
    else:
        print("Duplicate images", video_field_data["poster_image"])

with open("final_video.json", "w", encoding="utf-8") as outfile:
    json.dump(videos, outfile, ensure_ascii=False)