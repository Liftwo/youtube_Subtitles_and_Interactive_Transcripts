from django.shortcuts import redirect, render
from .forms import LinkForm
import requests
import xml.etree.ElementTree as et
import re
import json
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from visit.models import Visit, Like, Collect
from youtube_transcript_api import YouTubeTranscriptApi


class Upload:
    def lang_list(self, link):
        yt_url = link  # "https://www.youtube.com/watch?v=HMJiX77z4AU&t=851s&ab_channel=ITZY"
        match = re.search(r"youtube\.com/.*v=([^&]*)", yt_url)
        if match:
            video_id = match.group(1)
        else:
            video_id = ""
        api_key = "AIzaSyCfR-UnJRc8KmI9Y2sBr68r2Q93C_DJiUM"
        lang_list_url = f"https://youtube.googleapis.com/youtube/v3/captions?part=snippet&videoId={video_id}&key={api_key}"
        all_lang_code = []
        r = requests.get(lang_list_url)
        res = json.loads(r.content)
        print('這裏先',res)
        for i in res['items']:
            all_lang_code.append(i['snippet']['language'])
        all_lang_code.extend([video_id])
        print('這裏', all_lang_code)
        return all_lang_code  # id在list的最後

    def subtitles_xml(self, link):
        lang_code_list = self.lang_list(link)
        video_id = lang_code_list[-1]
        all_zh_sub = [i for i in lang_code_list if "zh" in i]
        all_en_sub = [i for i in lang_code_list if "en" in i]
        filter_en = []
        for i in all_en_sub:
            en = re.match("e\w+", i)
            if en:
                filter_en.append("en")

        zh_sub_order = ["zh-TW", "zh-HK", "zh-Hans", "zh", "zh-CN", "zh-Hant"]
        zh_sub = ""
        for i in range(0, 6):
            if zh_sub_order[i] in all_zh_sub:
                zh_sub = zh_sub_order[i]
                break
            else:
                continue

        return video_id, zh_sub, lang_code_list, filter_en  # id在前

    def subtitles(self, videoid, language):
        start = []
        dur = []
        end = []
        sub = []

        try:
            srt = YouTubeTranscriptApi.get_transcript(videoid, languages=[language])
        except:
            reminder = "Error"
            return reminder
        for elem in srt:  # loop all lines
            start.append(float(elem['start']))
            dur.append(float(elem['duration']))
            sub.append(elem['text'].replace('\n', ' '))

        for i, j in zip(start, dur):
            end.append(i + j)
        list_3 = [start, end, sub]

        return list_3

    def combine_sub(self, sub_en, sub_ch):
        df_en = pd.DataFrame({'start': sub_en[0], 'end': sub_en[1], 'text': sub_en[2]})
        df_ch = pd.DataFrame({'start': sub_ch[0], 'end': sub_ch[1], 'text': sub_ch[2]})
        df = pd.merge(df_en, df_ch, on='start')
        df = df.drop(columns=['end_y'], axis=1)
        df.columns = ['start', 'end', 'text_en', 'text_ch']
        sub_and_rate = []
        sub_and_rate.extend([len(df) / max(len(df_en), len(df_ch)), df.to_dict(orient='records')])
        return sub_and_rate

    def main(self, link):
        en_sub = self.subtitles(self.subtitles_xml(link)[0], "en")
        zh_sub = self.subtitles(self.subtitles_xml(link)[0], self.subtitles_xml(link)[1])
        return self.combine_sub(en_sub, zh_sub)

    def video_title(self, video_id):
        api_key = "AIzaSyCfR-UnJRc8KmI9Y2sBr68r2Q93C_DJiUM"
        path = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={video_id}&key={api_key}"
        r = requests.get(path)
        data = r.json()
        data_item = data['items'][0]
        title = data_item['snippet']['title']
        return title

    def visitor_count(self, request):
        request.session.set_expiry(60)
        if "like" not in request.session:
            request.session["like"] = True
            visit_model = Visit.objects.get(pk=1)
            visit_model.times += 1
            visit_model.save()
        else:
            visit_model = Visit.objects.get(pk=1)
            visit_model.times += 0
            visit_model.save()

        return visit_model.times


    def like_count(self, request):
        print(request.POST)
        likes = Like.objects.get(pk=1)
        if request.method == 'POST':
            likes_total = request.POST.get('likes', '')
            print(likes_total)
            likes.like_times = likes_total
            likes.save()
            likes_total = likes.like_times

        else:
            likes_total = likes.like_times
        return likes_total


yt = Upload()


def homepage(request):
    if "send_url" in request.POST:
        form = LinkForm(request.POST)
        if form.is_valid():
            link = request.POST['link']
            try:
                print(yt.subtitles_xml(link))
                video_id = yt.subtitles_xml(link)[0]
                request.session['link'] = link
                return redirect('upload', video_id=video_id)
            except:
                print(yt.subtitles_xml(link))
                return render(request, 'linkerror.html')

    form = LinkForm()
    visitor = yt.visitor_count(request)
    likes_total = yt.like_count(request)

    context = {'form': form, 'visitor': visitor, 'like_count': likes_total}
    return render(request, 'homepage.html', context)


def quote(string):
    return "'{}'".format(string)


def upload(request, video_id):
    link = request.session.get('link')
    code_list = yt.subtitles_xml(link)[2]
    zh_list = yt.subtitles_xml(link)[1]
    language = "en"
    if "Error" in yt.subtitles(video_id, language) or video_id == "": #代表影片遭刪除
        return render(request, 'linkerror.html')
    elif "en" not in code_list:
        check = code_list
        context = {'en': check}
        return render(request, 'linkerror.html', context)
    else:
        match_string = "^.*zh.*$"
        match_result = re.match(match_string, ''.join(zh_list))
        if not match_result:
            return render(request, 'linkerror.html')
        else:
            sub_dual = yt.\
                main(link)
            json_dual = json.dumps(sub_dual[1])
            rate = '%d%%' % int(sub_dual[0]*100)
            video_id = video_id
            title = yt.video_title(video_id)
            likes_total = yt.like_count(request)
            visitor = yt.visitor_count(request)
            context = {'json_dual': json_dual, 'video_id': video_id, 'rate': rate, 'video_title': title, 'visitor': visitor, 'like_count': likes_total}
            return render(request, 'result.html', context)


def about(request):
    likes_total = yt.like_count(request)
    visitor = yt.visitor_count(request)
    context = {'title':"It's a simple life.", 'visitor': visitor, 'like_count': likes_total}
    return render(request, 'about.html', context)


def collect(request):
    likes_total = yt.like_count(request)
    visitor = yt.visitor_count(request)
    context = {'visitor': visitor, 'like_count': likes_total}
    return render(request, 'collect_2.html', context)


def single_collect(request, pk):
    video_collect = Collect.objects.get(id=pk)
    likes_total = yt.like_count(request)
    visitor = yt.visitor_count(request)

    return render(request, 'single_collect.html', locals())



