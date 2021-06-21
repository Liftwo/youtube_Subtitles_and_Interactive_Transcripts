from django.shortcuts import redirect, render
from .forms import LinkForm
import requests
import xml.etree.ElementTree as et
import re
import json
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from visit.models import Visit, Like


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
    return id_and_url


def subtitles(xml):
    start = []
    dur = []
    end = []
    sub = []

    r = requests.get(xml)
    if (str(r.content) == "b''") or (str(r.content) == ""):
        list_3 = 'nothing'
    else:
        video_xml = et.fromstring(r.content)
        for elem in video_xml:  # loop all lines
            start.append(float(elem.attrib['start']))
            dur.append(float(elem.attrib['dur']))
            sub.append(elem.text.replace('\n', ' '))

        for i, j in zip(start, dur):
            end.append(i + j)
        list_3 = [start, end, sub]

    return list_3


def combine_sub(sub_en, sub_ch):
    df_en = pd.DataFrame({'start':sub_en[0], 'end':sub_en[1], 'text':sub_en[2]})
    df_ch = pd.DataFrame({'start':sub_ch[0], 'end':sub_ch[1], 'text':sub_ch[2]})
    df = pd.merge(df_en, df_ch, on='start')
    df = df.drop(columns=['end_y'], axis=1)
    df.columns = ['start', 'end', 'text_en', 'text_ch']
    sub_and_rate = []
    sub_and_rate.extend([len(df) / max(len(df_en), len(df_ch)), df.to_dict(orient='records')])
    return sub_and_rate


def main(link):
    zh_TW_sub = subtitles(subtitles_xml(link)[1][0]) #台灣繁體
    en_sub = subtitles(subtitles_xml(link)[1][3])
    hans_sub = subtitles(subtitles_xml(link)[1][1]) #zh-Hans
    zh_sub = subtitles(subtitles_xml(link)[1][2]) #zh
    if zh_TW_sub != 'nothing':
        ch_sub = zh_TW_sub
    elif hans_sub != 'nothing':
        ch_sub = hans_sub
    else:
        ch_sub = zh_sub
    return combine_sub(en_sub, ch_sub)


def visitor_count(request):
    if "like" not in request.session:
        request.session["like"]=True
        visit_model = Visit.objects.get(pk=1)
        visit_model.times +=1
        visit_model.save()
    else:
        visit_model = Visit.objects.get(pk=1)
        visit_model.times +=0
        visit_model.save()

    return visit_model.times


@csrf_exempt
def like_count(request):
    print(request.POST)
    likes = Like.objects.get(pk=1)
    if request.method == 'POST':
        likes_total = request.POST.get('likes','')
        print(likes_total)
        likes.like_times = likes_total
        likes.save()
        likes_total = likes.like_times

    else:
        likes_total = likes.like_times
    return likes_total

@csrf_exempt
def homepage(request):
    if "send_url" in request.POST:
        form = LinkForm(request.POST)
        if form.is_valid():
            link = request.POST['link']
            video_id = subtitles_xml(link)[0]
            request.session['link'] = link

            return redirect('upload', video_id=video_id)

    # elif "like" in request.POST:
    #     likes.like_times += 1
    #     likes.save()
    #     return redirect('homepage')

    form = LinkForm()
    visitor = visitor_count(request)
    likes_total = like_count(request)
    context = {'form': form, 'visitor': visitor, 'like_count': likes_total}
    return render(request, 'homepage.html', context)


def quote(string):
    return "'{}'".format(string)


def video_title(video_id):
    api_key = "AIzaSyCfR-UnJRc8KmI9Y2sBr68r2Q93C_DJiUM"
    path = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={video_id}&key={api_key}"
    r = requests.get(path)
    data = r.json()
    data_item = data['items'][0]
    title = data_item['snippet']['title']
    return title


def upload(request, video_id):
    link = request.session.get('link')
    r = requests.get(subtitles_xml(link)[1][3]) #en
    yt_video_id = subtitles_xml(link)[0]
    if "Error 404" in str(r.content) or yt_video_id == "" or str(r.content) == "b''": #代表影片遭刪除
        # reason = []
        # if "Error 404" in str(r.content):
        #     reason.append("404")
        # elif yt_video_id == "":
        #     reason.append("no id")
        # elif str(r.content) == "b''":
        #     reason.append('bb')
        # else:
        #     reason.append('else')
        # context={"reason":reason}
        return render(request, 'linkerror.html')
    else:
        sub_dual = main(link)
        json_dual = json.dumps(sub_dual[1])
        rate = '%d%%' % int(sub_dual[0]*100)
        video_id = video_id
        title = video_title(video_id)
        context = {'json_dual': json_dual, 'video_id': video_id, 'rate': rate, 'video_title': title}
        return render(request, 'result.html', context)


def about(request):
    likes_total = like_count(request)
    visitor = visitor_count(request)
    context = {'title':"It's a simple life.", 'visitor': visitor, 'like_count': likes_total}
    return render(request, 'about.html', context)


def collect(request):
    likes_total = like_count(request)
    visitor = visitor_count(request)
    context = {'visitor': visitor, 'like_count': likes_total}
    return render(request, 'collect_2.html', context)


def test(request):
    return render(request, 'test.html')


