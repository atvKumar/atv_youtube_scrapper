import json
import contextlib
from urllib.request import urlopen
from os.path import exists


def getfile(url,filename,timeout=60):
    with contextlib.closing(urlopen(url,timeout=timeout)) as fp:
        block_size = 1024 * 8
        block = fp.read(block_size)
        if block:
            with open(filename,'wb') as out_file:
                out_file.write(block)
                while True:
                    block = fp.read(block_size)
                    if not block:
                        break
                    out_file.write(block)
        else:
            raise Exception ('nonexisting file or connection error')

def download_file(url, filename):
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as fp:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                fp.write(chunk)
                fp.flush()


with open("thisone.json", encoding="utf-8") as json_file:
    data = json.load(json_file)

def download_playlist_thumbnails():
    for playlist in data:
        # print(playlist, "|", data[playlist]["slug"], data[playlist]["url"])
        playlist_thumb_file = f"playlist_thumbnail\\{data[playlist]['slug']}.jpg"
        getfile(data[playlist]["thumbnail"], playlist_thumb_file)
        print(f"Downloading {playlist} | {data[playlist]['slug']} | {data[playlist]['slug']}.jpg")
        for video in data[playlist]['items']:
            video_thumbnail_file = f"{data[playlist]['items'][video]['slug']}.jpg"
            if not exists(f"video_thumbnail\\{video_thumbnail_file}"):
                getfile(data[playlist]['items'][video]['thumbnail'], f"video_thumbnail\\{video_thumbnail_file}")
                cmd = f"curl -o video_thumbnail\\{video_thumbnail_file} {data[playlist]['items'][video]['thumbnail']}\n"
                with open("curl_batch.bat", 'a') as fp:
                    fp.writelines(cmd)
                print(video, video_thumbnail_file)
        print("\n")

download_playlist_thumbnails()