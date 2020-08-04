import requests
import urllib3
import time
from get_city_id import run
from videos_get import user_get
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
    传入城市id与城市名称，进行请求，获取数据，将数据list返回
    :param city:
    :return:
    '''
    min_t, max_t = timestamp()
    headers = {'Connection': 'keep-alive',
               'Cookie': 'd_ticket=4c5b44a063bf078fae71bffec25ddad8ca4ea; sid_guard=a6001040b2e52133062ca1e743097c06%7C1588771917%7C5183999%7CSun%2C+05-Jul-2020+13%3A31%3A56+GMT; uid_tt=de424823d2132aab28fa581760578e06; uid_tt_ss=de424823d2132aab28fa581760578e06; sid_tt=a6001040b2e52133062ca1e743097c06; sessionid=a6001040b2e52133062ca1e743097c06; sessionid_ss=a6001040b2e52133062ca1e743097c06; install_id=4019449375779358; ttreq=1$4e594dc75197827452871cc4798ece9879de8c47; odin_tt=0f3b487ba157b975aad4b8e1d04c17052757402df2bf93ef7960e47294225e4908eac12041c60548f61ed79e0b262cc3',
               'X-SS-REQ-TICKET': max_t,
               'X-Tt-Token': '00a6001040b2e52133062ca1e743097c062799657ae50f919ce3a8ff438f49a430bd781233129a06dd826624e23e1c61fc15',
               'sdk-version': '1', 'X-SS-DP': '1128',
               'x-tt-trace-id': '00-fdff35a10d9c7aafc2c264752dcc0468-fdff35a10d9c7aaf-01',
               'User-Agent': 'com.ss.android.ugc.aweme/100901 (Linux; U; Android 5.1.1; zh_CN; SM-N960F; Build/JLS36C; Cronet/TTNetVersion:8109b77c 2020-04-15 QuicVersion:0144d358 2020-03-24)',
               'Accept-Encoding': 'gzip', 'X-Gorgon': '0404704340018db90ce28bf4d04e178d69e587f9050da34202e2',
               'X-Khronos': min_t}
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get(url, headers=headers, verify=False).json()
        result = response['aweme_list']
    except:
        result = None
    return result


def result_parse(result, city):
    production_list = []
    try:
        for aweme in result:
            try:
                author_sec_uid = aweme['author']['sec_uid']
                production_dict = {
                    'author_sec_uid': author_sec_uid,
                    'city_id': city['city_id'],
                    'city_name': city['city_name']
                }

                production_list.append(production_dict)
            except:
                pass
    except:
        pass

    return production_list


def run_data():
    '''
    :return:
    '''
    city_list = run()
    for city in city_list:
        try:
            city_id = city['city_id']
            city_name = city['city_name']
            min_t, max_t = timestamp()
            url = 'https://api3-core-c-lq.amemv.com/aweme/v1/nearby/feed/?max_cursor=0&min_cursor=0&count=20&feed_style=1' \
                  '&filter_warn=0&city={}&latitude=31.99879076689188&longitude=100.5647239604455&poi_class_code=0&pull_type=1' \
                  '&location_permission=1&nearby_distance=0&roam_city_name={' \
                  '}&insert_fresh_aweme_ids&insert_fresh_type=0&os_api=22&device_type=SM-N960F&ssmix=a&manifest_version_code' \
                  '=100901&dpi=240&uuid=355757648741243&app_name=aweme&version_name=10.9.0&ts={}&app_type=normal&ac' \
                  '=wifi&host_abi=armeabi-v7a&update_version_code=10909900&channel=tengxun_new&_rticket=1589104292895' \
                  '&device_platform=android&iid=4019449375779358&version_code=100900&cdid=1421f378-62fa-44ad-af4f' \
                  '-49d33aa7a58a&openudid=9a7fc881896f46bf&device_id=2752811979515463&resolution=720*1280&os_version=5.1.1' \
                  '&language=zh&device_brand=samsung&aid=1128&mcc_mnc=46007'.format(city_id, city_name, min_t)
            data = get_data(url)
            result = result_parse(data, city)
            # 循环列表对每个用户进行所有作品抓取
            for user in result:
                p = Process(target=user_get, args=(user, ))
                p.start()
        except:
            pass

