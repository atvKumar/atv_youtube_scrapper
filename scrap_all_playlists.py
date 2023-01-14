import os
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    # client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"
    DEVELOPER_KEY = ""  # Enter your Key here

    # Get credentials and create an API client
    # flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    #     client_secrets_file, scopes)
    # credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.playlists().list(
        part="snippet,contentDetails, status",
        channelId="UCVRh_8fyUuMj7Tuqp5O3HpA",
        maxResults=50,
        # pageToken="CBkQAA",
        prettyPrint=True
    )
    response = request.execute()
    # print(response["nextPageToken"])
    # json_object = json.dumps(response, indent = 4) 
    # print(json_object)
    no = 1
    combine = dict() | response
    # with open(f"Created_Playlist{no}.json", "w", encoding="utf-8") as outfile:
    #     json.dump(response, outfile, ensure_ascii=False)

    try:
        while response["nextPageToken"]:
            request = youtube.playlists().list(
                part="snippet,contentDetails, status",
                channelId="UCVRh_8fyUuMj7Tuqp5O3HpA",
                maxResults=50,
                pageToken=response["nextPageToken"],
                prettyPrint=True
            )
            response = request.execute()
            combine["items"] = combine["items"] + response["items"]
            no +=1
            # with open(f"Created_Playlist{no}.json", "w", encoding="utf-8") as outfile:
            #     json.dump(response, outfile, ensure_ascii=False)
    except KeyError:
        print(f"Completed Scrapping All {no} Playlists...")
        with open("All_Playlists.json", "w", encoding="utf-8") as outfile:
                json.dump(combine, outfile, ensure_ascii=False)

if __name__ == "__main__":
    main()
