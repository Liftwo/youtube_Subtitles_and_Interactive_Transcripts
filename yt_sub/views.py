from django.shortcuts import redirect, render
from datetime import timedelta
from .forms import LinkForm
from django.urls import reverse
from urllib.parse import urlencode
from django.contrib.sessions.models import Session
# from opencc import OpenCC
from srt import *
import requests
import xml.etree.ElementTree as et
import re
import json
import pandas as pd


def subtitles_xml(link):
    yt_url = link #"https://www.youtube.com/watch?v=HMJiX77z4AU&t=851s&ab_channel=ITZY"
    url_get_1 = yt_url.split("&")
    url_get_2 = url_get_1[0].split("=")
    video_id = url_get_2[1]
    subtitles_url = []
    subtitles_url.extend([f"http://www.youtube.com/api/timedtext?v={video_id}&lang=zh-Hans", f"http://www.youtube.com/api/timedtext?v={video_id}&lang=en"])
    id_and_url = [video_id]
    id_and_url.append(subtitles_url)
    return id_and_url


def subtitles(xml):
    start = []
    dur = []
    end = []
    sub = []
    # cc = OpenCC('s2tw')

    r = requests.get(xml)
    video_xml = et.fromstring(r.content)
    for elem in video_xml: #loop all lines
        start.append(float(elem.attrib['start']))
        dur.append(float(elem.attrib['dur']))
        sub.append(elem.text.replace('\n', ' '))

    for i, j in zip(start, dur):
        end.append(i+j)
    list_3 = [start, end, sub]
    return list_3


# def combine_sub(sub_en, sub_ch):
#     df_en = pd.DataFrame({'start':sub_en[0], 'end':sub_en[1], 'text':sub_en[2]})
#     df_ch = pd.DataFrame({'start':sub_ch[0], 'end':sub_ch[1], 'text':sub_ch[2]})
#     df = pd.merge(df_en, df_ch, on='start')
#     df['text'] = df['text_x']+'<br>'+df['text_y']
#     df = df.drop(columns=['end_y', 'text_x', 'text_y'], axis=1)
#     df.columns = ['start', 'end', 'text']
#     # df_list = [df['start'].tolist(), df['end'].tolist(), df['text'].tolist()]
#     d = df.to_dict(orient='records')
#     return d


def combine_sub(sub_en, sub_ch):
    df_en = pd.DataFrame({'start':sub_en[0], 'end':sub_en[1], 'text':sub_en[2]})
    df_ch = pd.DataFrame({'start':sub_ch[0], 'end':sub_ch[1], 'text':sub_ch[2]})
    df = pd.merge(df_en, df_ch, on='start')
    df = df.drop(columns=['end_y'], axis=1)
    df.columns = ['start', 'end', 'text_en', 'text_ch']
    # df_list = [df['start'].tolist(), df['end'].tolist(), df['text'].tolist()]
    d = df.to_dict(orient='records')
    return d

# def srt_file(list_3):
#     start = []
#     end = []
#     c = 1
#     subs = []
#     subs_js = []
#     for i, j,k in zip(list_3[0], list_3[1], list_3[2]):
#         start.append(timedelta(seconds=i))
#         end.append(timedelta(seconds=j))
#         d = {"start":i, "end":j, "text":k}
#         subs_js.append(d)
#     for i, j, k in zip(start, end, list_3[2]):
#         subs.append(Subtitle(index=c, start=i, end=j, content=k))
#         c += 1
#
#     srt = compose(subs)
#     return srt


def main(link):
    en_sub = subtitles(subtitles_xml(link)[1][1])
    ch_sub = subtitles(subtitles_xml(link)[1][0])

    return combine_sub(en_sub, ch_sub)


if __name__ == "__main__":
    main()


def homepage(request):
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            link = request.POST['link']
            video_id = subtitles_xml(link)[0]
            request.session['link'] = link
            # sub_dual = main(request.POST['link'])
            # json_dual = json.dumps(sub_dual)
            # context = {'json_dual': json_dual, 'video_id': video_id}

            # return render(request, 'linkerror.html', context)

            return redirect('upload', video_id=video_id)

        else:
            errors_notice = "網址格式不正確"
            form = LinkForm()
            context = {'form': form, 'notice': errors_notice}
            return render(request, 'homepage.html', context)
            # return redirect('/homepage/')

    form = LinkForm()
    notice = " "
    context = {'form': form, 'notice': notice}
    return render(request, 'homepage.html', context)


def upload(request, video_id):
    link = request.session.get('link')
    sub_dual = main(link)
    json_dual = json.dumps(sub_dual)
    video_url = "https://www.youtube.com/embed/" + video_id
    context = {'json_dual': json_dual, 'video_url': video_url, 'sub_dual': sub_dual}
    return render(request, 'test.html', context)


def fortest(request):
    return render(request, 'fortest.html')




