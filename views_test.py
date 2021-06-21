import requests
import xml.etree.ElementTree as et
import pandas as pd
import re


def subtitles_xml(link):
    yt_url = link  # "https://www.youtube.com/watch?v=HMJiX77z4AU&t=851s&ab_channel=ITZY"
    # url_get_1 = yt_url.split("&")
    # url_get_2 = url_get_1[0].split("=")
    # video_id = url_get_2[1]
    match = re.search(r"youtube\.com/.*v=([^&]*)", yt_url)
    if match:
        video_id = match.group(1)
    else:
        video_id = ""
    subtitles_url = []
    subtitles_url.extend([f"http://www.youtube.com/api/timedtext?v={video_id}&lang=zh-TW", f"http://www.youtube.com/api/timedtext?v={video_id}&lang=zh-Hans", f"http://www.youtube.com/api/timedtext?v={video_id}&lang=zh",f"http://www.youtube.com/api/timedtext?v={video_id}&lang=en"])
    id_and_url = [video_id]
    id_and_url.append(subtitles_url)
    print(id_and_url)

    return id_and_url

# r = requests.get(subtitles_xml("https://www.youtube.com/watch?v=1qX6YHBVDiQ")[1][2])
# print(r.content)


import requests
def upload(link):
    r = requests.get(subtitles_xml(link)[1][2]) #en
    yt_video_id = subtitles_xml(link)[0]
    if "Error 404" in str(r.content) or yt_video_id == "" or str(r.content) == "b''":
        print(r.content)
    else:
        print('n')



amber = "https://www.youtube.com/watch?v=1qX6YHBVDiQ"
upload(amber)


