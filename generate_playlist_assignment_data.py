import json
from datetime import datetime

with open("thisone.json", encoding="utf-8") as json_file:
    data = json.load(json_file)

result = []
# rest = []
for index, playlist in enumerate(data, 1):
    x = [video for video in data[playlist]["items"]]    
    for i in x:
        item = data[playlist]["items"][i]['Name']
        if item not in result:
            result.append(item)

video_list = {}
for i, vid in enumerate(result, 1):
    # print(i, vid)
    video_list[i] = vid

playlist_assignment = []
# for i in range(1, 3501):
#     # print(i)
#     playlist_item = {"model": "vod.playlist_assignment"}
#     playlist_item["pk"] = i
#     fields = {}
#     playlist_item['fields'] = fields
#     playlist_assignment.append(playlist_item)
def get_key(val):
    for key, value in video_list.items():
        if val == value:
            return key

today = f"{datetime.utcnow().replace(microsecond=0).isoformat()}.000Z"

pk = 1
for i, playlist_id in enumerate(data, 1):
    # print(i)
    playlist_item = {"model": "vod.playlist_assignment"}
    for item in data[playlist_id]['items']:
        playlist_item["pk"] = pk
        fields = {}
        fields['playlist_id'] = i
        playlist_video_name = data[playlist_id]['items'][item]['Name']
        fields['video_id'] = get_key(playlist_video_name)
        fields['timestamp'] = today
        fields['position'] = int(item)
        playlist_item['fields'] = fields
        playlist_assignment.append(playlist_item)
        print(f"{playlist_item},")
        pk = pk + 1

# with open("test.json", "w", encoding="utf-8") as outfile:
#     json.dump(playlist_assignment, outfile, ensure_ascii=False)