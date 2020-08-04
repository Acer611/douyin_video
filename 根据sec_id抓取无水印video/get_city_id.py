import requests
import urllib3


def run():
    url = 'https://api3-normal-c-lq.amemv.com/aweme/v1/city/list/?longitude=100.5647239604455&latitude=31.99879076689188&location_permission=1&os_api=22&device_type=SM-N960F&ssmix=a&manifest_version_code=100901&dpi=240&uuid=355757648741243&app_name=aweme&version_name=10.9.0&ts=1589103572&app_type=normal&ac=wifi&host_abi=armeabi-v7a&update_version_code=10909900&channel=tengxun_new&_rticket=1589103572570&device_platform=android&iid=4019449375779358&version_code=100900&cdid=1421f378-62fa-44ad-af4f-49d33aa7a58a&openudid=9a7fc881896f46bf&device_id=2752811979515463&resolution=720*1280&os_version=5.1.1&language=zh&device_brand=samsung&aid=1128&mcc_mnc=46007'
    headers = {'Connection': 'keep-alive',
               'Cookie': 'd_ticket=4c5b44a063bf078fae71bffec25ddad8ca4ea; sid_guard=a6001040b2e52133062ca1e743097c06%7C1588771917%7C5183999%7CSun%2C+05-Jul-2020+13%3A31%3A56+GMT; uid_tt=de424823d2132aab28fa581760578e06; uid_tt_ss=de424823d2132aab28fa581760578e06; sid_tt=a6001040b2e52133062ca1e743097c06; sessionid=a6001040b2e52133062ca1e743097c06; sessionid_ss=a6001040b2e52133062ca1e743097c06; install_id=4019449375779358; ttreq=1$4e594dc75197827452871cc4798ece9879de8c47; odin_tt=0f3b487ba157b975aad4b8e1d04c17052757402df2bf93ef7960e47294225e4908eac12041c60548f61ed79e0b262cc3',
               'X-SS-REQ-TICKET': '1589103572550',
               'X-Tt-Token': '00a6001040b2e52133062ca1e743097c062799657ae50f919ce3a8ff438f49a430bd781233129a06dd826624e23e1c61fc15',
               'sdk-version': '1', 'X-SS-DP': '1128',
               'x-tt-trace-id': '00-fdf437cf0d9c7aafc2c2647449fa0468-fdf437cf0d9c7aaf-01',
               'User-Agent': 'com.ss.android.ugc.aweme/100901 (Linux; U; Android 5.1.1; zh_CN; SM-N960F; Build/JLS36C; Cronet/TTNetVersion:8109b77c 2020-04-15 QuicVersion:0144d358 2020-03-24)',
               'Accept-Encoding': 'gzip', 'X-Gorgon': '0404704340015cf2abe18bf4d04e178d69e587f9050da3e20689',
               'X-Khronos': '1589103572'}
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = requests.get(url, headers=headers, verify=False).json()
    city_list = data_parse(response['all'])
    return city_list


def data_parse(data):
    city_list = []
    for city in data:
        # print(data)
        city_dict = {
            'city_id': city['code'],
            'city_name': city['name']
        }
        city_list.append(city_dict)

    return city_list
