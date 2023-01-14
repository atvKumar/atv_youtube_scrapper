import os
import json
import slugify
from private_playlists import blacklisted

with open("All_Playlists.json", encoding="utf-8") as json_file:
    data = json.load(json_file)

adjusted_data = dict()

xindex = 1
for item in data["items"]:
    playlist_index = f"playlist{xindex}"
    slug_filename = slugify.slugify(item["snippet"]["title"])
    print(playlist_index, "|", slug_filename)
    if f"{slug_filename}.json" not in blacklisted:
        adjusted_data[playlist_index] = {}
        adjusted_data[playlist_index]["Name"] = item["snippet"]["title"]
        adjusted_data[playlist_index]["slug"] = slug_filename
        adjusted_data[playlist_index]["filename"] = f"{slug_filename}.json"
        adjusted_data[playlist_index]["description"] = item["snippet"]["description"]
        adjusted_data[playlist_index]["date_uploaded"] = item["snippet"]["publishedAt"].replace('Z', '+00:00')
        
        with open(f"sub_playlist\\{slug_filename}.json", encoding="utf-8") as json_file:
            playlist_data = json.load(json_file)
        # if xindex == 94:
        #     print("\n    ", playlist_data["items"])
        try:
            videoID = playlist_data["items"][0]["contentDetails"]["videoId"]
            playlistID = playlist_data["items"][0]["snippet"]["playlistId"]
        except IndexError:
            videoID = ""
            playlistID = ""
        xindex += 1
        adjusted_data[playlist_index]["url"] = f"https://www.youtube.com/watch?v={videoID}&list={playlistID}"
        try:
            adjusted_data[playlist_index]["thumbnail"] = item["snippet"]["thumbnails"]["maxres"]["url"]
        except KeyError:
            adjusted_data[playlist_index]["thumbnail"] = item["snippet"]["thumbnails"]["high"]["url"]
        adjusted_data[playlist_index]["items"] = {}
        index = 1
        for sub_item in playlist_data["items"]:
            adjusted_data[playlist_index]["items"][index] = {}
            adjusted_data[playlist_index]["items"][index]["Name"] = sub_item["snippet"]["title"]
            adjusted_data[playlist_index]["items"][index]["slug"] = slugify.slugify(sub_item["snippet"]["title"])
            adjusted_data[playlist_index]["items"][index]["description"] = sub_item["snippet"]["description"]
            adjusted_data[playlist_index]["items"][index]["date_uploaded"] = sub_item["snippet"]["publishedAt"].replace('Z', '+00:00')
            videoID = sub_item["contentDetails"]["videoId"]
            adjusted_data[playlist_index]["items"][index]["url"] = f"https://www.youtube.com/watch?v={videoID}"
            adjusted_data[playlist_index]["items"][index]["videoID"] = videoID
            # print(index, sub_item["snippet"]["title"], "\n")
            try:
                # print("    ", sub_item["snippet"]["thumbnails"]["maxres"])
                adjusted_data[playlist_index]["items"][index]["thumbnail"] = sub_item["snippet"]["thumbnails"]["maxres"]["url"]
            except KeyError:
                # print(index, sub_item["snippet"]["thumbnails"]["standard"])
                try:
                    adjusted_data[playlist_index]["items"][index]["thumbnail"] = sub_item["snippet"]["thumbnails"]["standard"]["url"]
                except KeyError:  # No thumbnail found, possible Private Video
                    # TODO: explicit check for Private Video Title
                    del adjusted_data[playlist_index]["items"][index]
                    index -= 1
            index += 1
    else:
        xindex -= 1

with open("thisone.json", "w", encoding="utf-8") as outfile:
    json.dump(adjusted_data, outfile, ensure_ascii=False)