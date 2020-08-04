import os
import requests
import random
import time
import urllib3
from downloads import save
from multiprocessing import Process



def timestamp():
    '''
    生成时间戳
    :return:
    '''
    min_t = int(time.time())
    max_t = int(time.time() * 1000)
    return str(min_t), str(max_t)


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
    '''
    根据请求url获取数据
    :param url:
    :return:
    data:list数据
    max_cursor:下次请求需要携带的参数
    '''
    while True:
        min_t, max_t = timestamp()
        headers = {'Connection': 'keep-alive',
                   'Cookie': 'd_ticket=4c5b44a063bf078fae71bffec25ddad8ca4ea; odin_tt=6450ec41def6afd0731d426731b508fcf43650505f50460244a368ac5847f0d1cbf6747a7ad4e89fa3b0f0e15754002e; sid_guard=a6001040b2e52133062ca1e743097c06%7C1588771917%7C5183999%7CSun%2C+05-Jul-2020+13%3A31%3A56+GMT; uid_tt=de424823d2132aab28fa581760578e06; uid_tt_ss=de424823d2132aab28fa581760578e06; sid_tt=a6001040b2e52133062ca1e743097c06; sessionid=a6001040b2e52133062ca1e743097c06; sessionid_ss=a6001040b2e52133062ca1e743097c06; install_id=4019449375779358; ttreq=1$4e594dc75197827452871cc4798ece9879de8c47',
                   'X-SS-REQ-TICKET': '1588773397905',
                   'X-Tt-Token': '00a6001040b2e52133062ca1e743097c06cdb862c09a8bd8d850534d8a1ddf1bcda1297dfe483093add3539ae384dd657413',
                   'sdk-version': '1',
                   'X-SS-DP': '1128',
                   'x-tt-trace-id': '00-ea46271a0d9c7aafc2c2647f8e990468-ea46271a0d9c7aaf-01',
                   'User-Agent': 'com.ss.android.ugc.aweme/100901 (Linux; U; Android 5.1.1; zh_CN; SM-N960F; Build/JLS36C; Cronet/TTNetVersion:8109b77c 2020-04-15 QuicVersion:0144d358 2020-03-24)',
                   'Accept-Encoding': 'gzip',
                   'X-Gorgon': '0404b8014001a0ff70a608a72b1c1754b85bab86f700fceac8f4',
                   'X-Khronos': min_t,
                   'x-common-params-v2': 'os_api=22&device_platform=android&device_type=SM-N960F&iid=4019449375779358&version_code=100900&app_name=aweme&openudid=9a7fc881896f46bf&device_id=2752811979515463&os_version=5.1.1&aid=1128&channel=tengxun_new&ssmix=a&manifest_version_code=100901&dpi=240&cdid=1421f378-62fa-44ad-af4f-49d33aa7a58a&version_name=10.9.0&resolution=720*1280&language=zh&device_brand=samsung&app_type=normal&ac=wifi&update_version_code=10909900&uuid=355757648741243'}
        try:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            response = requests.get(url, headers=headers, verify=False).json()
            max_cursor = response['max_cursor']
            if not response['aweme_list']:
                pass
            else:
                data = response['aweme_list']
                return data, max_cursor
        except:
            data = None
            max_cursor = None
            return data, max_cursor


def data_parse(data):
    '''
    用户作品数据解析
    :param data:
    :return:
    '''
    production_list = []
    for i in data:
        production_dict = {
            'user_name': i['author']['nickname'],
            'desc': i['desc'],
            'time': fabu_time(i['create_time']),
            'music_author': i['music']['author'],
            'music_name': i['music']['title'],
            'video_url': i['video']['play_addr_lowbr']['url_list'][0]
        }
        production_list.append(production_dict)
    return production_list


def user_get(user):
    '''
    传入目标用户的sec_uid对单个用户循环抓取所有作品
    :param sec_uid:
    :return:
    '''
    sec_id = user['author_sec_uid']
    city_name = user['city_name']
    max_cursor = 0
    while True:
        min_t, max_t = timestamp()
        url = 'https://api3-normal-c-lq.amemv.com/aweme/v1/aweme/post/?source=0&publish_video_strategy_type=0&max_cursor={}&sec_user_id={}&count=20&ts={}&host_abi=armeabi-v7a&_rticket={}&mcc_mnc=46007&'.format(
            max_cursor, sec_id, min_t, max_t)
        data, max_cursor = get_data(url)
        if data is not None and max_cursor is not None:
            production_list = data_parse(data)
            for production in production_list:
                print('正在对数据进行保存本地操作，请稍等片刻！')
                p = Process(target=save, args=(production, city_name))
                p.start()


        else:
            print('当前用户已抓完！')
            break



