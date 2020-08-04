
import os
import requests
import random
import time
import urllib3


def timestamp():
    '''
    生成时间戳
    :return:
    '''
    s = time.time()
    min_t = int(s)
    max_t = int(s * 1000)
    return str(min_t), str(max_t)


def attention_me_uid(url):
    '''
    获取我关注的用户的uid与下一页请求锁需要的参数
    :return:
    '''
    while True:
        min_t, max_t = timestamp()
        headers = {'Connection': "keep-alive",
                   'Cookie': 'd_ticket=4c5b44a063bf078fae71bffec25ddad8ca4ea; odin_tt=6450ec41def6afd0731d426731b508fcf43650505f50460244a368ac5847f0d1cbf6747a7ad4e89fa3b0f0e15754002e; sid_guard=a6001040b2e52133062ca1e743097c06%7C1588771917%7C5183999%7CSun%2C+05-Jul-2020+13%3A31%3A56+GMT; uid_tt=de424823d2132aab28fa581760578e06; uid_tt_ss=de424823d2132aab28fa581760578e06; sid_tt=a6001040b2e52133062ca1e743097c06; sessionid=a6001040b2e52133062ca1e743097c06; sessionid_ss=a6001040b2e52133062ca1e743097c06; install_id=4019449375779358; ttreq=1$4e594dc75197827452871cc4798ece9879de8c47',
                   'X-SS-REQ-TICKET': max_t,
                   'X-Tt-Token': '00a6001040b2e52133062ca1e743097c06cdb862c09a8bd8d850534d8a1ddf1bcda1297dfe483093add3539ae384dd657413',
                   'sdk-version': '1',
                   'X-SS-DP': '1128',
                   'x-tt-trace-id': '00-ea7df3860d9c7aafc2c2647233a00468-ea7df3860d9c7aaf-01',
                   'User-Agent': 'com.ss.android.ugc.aweme/100901 (Linux; U; Android 5.1.1; zh_CN; SM-N960F; Build/JLS36C; Cronet/TTNetVersion:8109b77c 2020-04-15 QuicVersion:0144d358 2020-03-24)',
                   'Accept-Encoding': 'gzip',
                   'X-Gorgon': '0404b8014001fc330e5d08a72b1c1754b85bab86f700fca29ee3',
                   'X-Khronos': min_t,
                   'x-common-params-v2': 'os_api=22&device_platform=android&device_type=SM-N960F&iid=4019449375779358&version_code=100900&app_name=aweme&openudid=9a7fc881896f46bf&device_id=2752811979515463&os_version=5.1.1&aid=1128&channel=tengxun_new&ssmix=a&manifest_version_code=100901&dpi=240&cdid=1421f378-62fa-44ad-af4f-49d33aa7a58a&version_name=10.9.0&resolution=720*1280&language=zh&device_brand=samsung&app_type=normal&ac=wifi&update_version_code=10909900&uuid=355757648741243'}
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get(url, headers=headers, verify=False).json()
        print(response)
        try:
            max_time = response['max_time']
            if not response['followings']:
                pass
            else:
                data = response['followings']
                return data, max_time
        except:
            data = None
            max_cursor = None
            return data, max_cursor


if __name__ == '__main__':
    max_time = 1588778511
    while True:
        min_t, max_t = timestamp()
        url = 'https://api3-normal-c-lq.amemv.com/aweme/v1/user/following/list/?user_id=86304636253&sec_user_id=MS4wLjABAAAAliUfImgLRYe1ih0ZL0_GQ3dzUAOGZ1JEInos9icA04w&max_time={}&count=20&offset=0&source_type=2&address_book_access=2&gps_access=1&vcd_count=0&vcd_auth_first_time=0&ts={}&host_abi=armeabi-v7a&_rticket={}&mcc_mnc=46007&'.format(
            max_time, min_t, max_t)
        print(url)
        data, max_time = attention_me_uid(url)
        time.sleep(2)