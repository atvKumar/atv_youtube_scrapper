# -----------------------------------------------------------------------------
# Generate Playlist Data Fixture to be imported into Django vod_backend APP
# -----------------------------------------------------------------------------
import json

# Load the extracted and prepared data from extract_playlist_data.py
with open("thisone.json", encoding="utf-8") as json_file:
    data = json.load(json_file)

playlist_data = []
for index, playlist in enumerate(data, 1):
    # print(data[playlist]["Name"])
    # break
    playlist_item = {"model": "vod.playlist", "pk": index}
    playlist_field_data = {}
    playlist_field_data["title"] = data[playlist]["Name"]
    playlist_field_data["slug"] = data[playlist]["slug"]
    playlist_field_data["short_description"] = data[playlist]["description"]
    playlist_field_data["poster_image"] = f"playlist_thumbnail/{data[playlist]['slug']}.jpg"
    playlist_field_data["external_url"] = data[playlist]["url"]
    playlist_field_data["status"] = "Public"
    playlist_field_data["language_id"] = data[playlist]["language"]
    playlist_item["fields"] = playlist_field_data
    playlist_data.append(playlist_item)

# print(playlist_data)
with open("final_playlist.json", "w", encoding="utf-8") as outfile:
    json.dump(playlist_data, outfile, ensure_ascii=False)