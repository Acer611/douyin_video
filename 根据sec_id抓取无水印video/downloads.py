import random
import config
import os
import requests


def save(dict, city_name):
    '''
    传入字典保存数据
    :param dict:
    :return:
    '''
    print('数据进入保存模块，正在进行本地存储。')
    print(dict)

    # 有些作品中没有标题导致我们再保存数据时会覆盖，所以我们对没有标题的作品进行命名
    num = str(random.randint(0, 100))
    if dict['desc'] == '':
        name = dict['user_name'] + '的作品{}'.format(num) + '.mp4'
    else:
        name = dict['desc'] + '.mp4'
    video_url = dict['video_url']
    try:
        res = requests.get(video_url)
        file_name = config.save_video_path+'/'+ city_name +'/'+dict['user_name']+'/'+name
        # 判断城市文件夹是否存在
        if os.path.exists(config.save_video_path+'/'+ city_name):
            # 判断用户文件夹是否存在
            if os.path.exists(config.save_video_path+'/'+ city_name +'/'+dict['user_name']):

                with open(file_name, 'wb') as f:
                    f.write(res.content)

            else:
                os.mkdir(config.save_video_path+'/'+ city_name +'/'+dict['user_name'])
                with open(file_name, 'wb') as f:
                    f.write(res.content)
        else:
            os.mkdir(config.save_video_path+'/'+ city_name)
            os.mkdir(config.save_video_path+'/'+ city_name+'/'+dict['user_name'])
            with open(file_name, 'wb') as f:
                f.write(res.content)

    except:
        pass