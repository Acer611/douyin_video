# -*- coding: utf-8 -*-
import os
import requests
import json
import time
import urllib3


def timestamp():
    '''
    生成时间戳
    :return:
    '''
    t = int(time.time())
    return str(t)


def fabu_time(t):
    '''
    将时间戳转换成时间格式
    :param t:
    :return:
    '''
    timeArray = time.localtime(t)
    fabu_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return fabu_time


def get_data(url):
    headers = {'Connection': 'keep-alive',
               'Cookie': 'install_id=4019449375779358; ttreq=1$4e594dc75197827452871cc4798ece9879de8c47; passport_csrf_token=37b7163131512945c98328dc89518dde; d_ticket=8a2770a7dd286c956e1fdace2eb9b4d4ca4ea; odin_tt=eea31e1660bf63c6461e82261695e924b710d85c8a3b142c9b648193d7a5d8075c4dcf75011903af1faa3ee4e78725d7bdc6a195d4d97b9f5a61c94ff999ab04; sid_guard=145242f4fcabba481f479a33d1e85ca0%7C1588667279%7C5184000%7CSat%2C+04-Jul-2020+08%3A27%3A59+GMT; uid_tt=d6596917291e4380f488b3042c052e86; uid_tt_ss=d6596917291e4380f488b3042c052e86; sid_tt=145242f4fcabba481f479a33d1e85ca0; sessionid=145242f4fcabba481f479a33d1e85ca0; sessionid_ss=145242f4fcabba481f479a33d1e85ca0',
               'X-SS-REQ-TICKET': '1588667688341',
               'X-Tt-Token': '00145242f4fcabba481f479a33d1e85ca0f9843c8f7a6ff6a8674c8fae1afd497d6ace379c0cf3260a2dc749620266e12b1f',
               'sdk-version': '1',
               'X-SS-DP': '1128',
               'x-tt-trace-id': '00-e3f927390d9c7aafc2c2647efc4d0468-e3f927390d9c7aaf-01',
               'User-Agent': 'com.ss.android.ugc.aweme/100901 (Linux; U; Android 5.1.1; zh_CN; SM-N960F; Build/JLS36C; Cronet/TTNetVersion:8109b77c 2020-04-15 QuicVersion:0144d358 2020-03-24)',
               'Accept-Encoding': 'gzip',
               'X-Gorgon': '040438a1400170f54d1c9c982cba73781a00368731768f816295',
               'X-Khronos': timestamp()}

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = requests.get(url, headers=headers, verify=False).json()
    resp_list = response['aweme_list']
    video_list = []
    for resp in resp_list:
        try:
            create_time = resp['create_time']

            author_uid = resp['author']['uid']

            author_name = resp['author']['nickname']

            title = resp['desc']

            video_url = resp['video']['download_suffix_logo_addr']['url_list'][0]
            video_dict = {
                'author_name': author_name,
                'author_uid': author_uid,
                'title': title,
                'time': fabu_time(create_time),
                'video_url': video_url
            }

            video_list.append(video_dict)
        except:
            pass
    return video_list


def downloads_video(video_dict):
    name = video_dict['title'] + '.mp4'
    video_url = video_dict['video_url']
    res = requests.get(video_url)
    file_name = 'D:/code/抖音App/videos/' + name

    with open(file_name, 'wb') as f:
        f.write(res.content)
        print('{}下载完成！'.format(name))


if __name__ == '__main__':
    while True:
        try:
            t = timestamp()
            url = 'https://api3-core-c-lq.amemv.com/aweme/v1/nearby/feed/?max_cursor=0&min_cursor=0&count=20&feed_style=1&filter_warn=0&city=110000&latitude=31.99879076689188&longitude=100.5647239604455&poi_class_code=0&pull_type=1&location_permission=1&nearby_distance=0&roam_city_name=%E5%8C%97%E4%BA%AC&insert_fresh_aweme_ids&insert_fresh_type=0&os_api=22&device_type=SM-N960F&ssmix=a&manifest_version_code=100901&dpi=240&uuid=355757648741243&app_name=aweme&version_name=10.9.0&ts={}0&app_type=normal&ac=wifi&host_abi=armeabi-v7a&update_version_code=10909900&channel=tengxun_new&_rticket=1588783161264&device_platform=android&iid=4019449375779358&version_code=100900&cdid=1421f378-62fa-44ad-af4f-49d33aa7a58a&openudid=9a7fc881896f46bf&device_id=2752811979515463&resolution=720*1280&os_version=5.1.1&language=zh&device_brand=samsung&aid=1128&mcc_mnc=46007'.format(t)
            video_list = get_data(url)
            for video_dict in video_list:

                downloads_video(video_dict)
            time.sleep(5)
        except:
            time.sleep(5)
