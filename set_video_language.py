# -----------------------------------------------------------------------------
# Read language Manually set from thisone.json Playlist and appy to all items
# -----------------------------------------------------------------------------
import json

# Load the extracted and prepared data from extract_playlist_data.py
with open("thisone.json", encoding="utf-8") as json_file:
    data = json.load(json_file)

for index, playlist in enumerate(data, 1):
    # print(playlist, data[playlist]['Name'], data[playlist]['language'])
    playlist_language = data[playlist]['language']
    for video in data[playlist]['items']:
        # print(playlist, data[playlist]['items'][video]['Name'])
        data[playlist]['items'][video]['language'] = playlist_language

with open("thisone.json", "w", encoding="utf-8") as outfile:
    json.dump(data, outfile, ensure_ascii=False)