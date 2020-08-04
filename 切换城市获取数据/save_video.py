import requests
import os
import random
import dy_settings


def save(video_dict):
    '''
    保存数据到本地:将不同城市得数据保存到对应的城市文件夹下
    :param video_dict:
    :return:
    '''
    try:
        # 城市名
        city_name= video_dict['city_name']
        # video名
        num = str(random.randint(0, 100))
        if video_dict['title'] == '':
            name = video_dict['user_name'] + '的作品{}'.format(num) + '.mp4'
        else:
            name = video_dict['title'] + '.mp4'
        video_url = video_dict['video_url']
        res = requests.get(video_url)
        file_name = dy_settings.save_path+city_name+'/'+name
        if os.path.exists(dy_settings.save_path+city_name):
            if os.path.exists(file_name):
                try:
                    with open(file_name, 'wb') as f:
                        f.write(res.content)
                        print('作品{}已抓取完成并保存到本地。。。'.format(name))
                except:
                    print('保存失败!!！')
            else:
                pass
        else:
            try:
                os.mkdir(dy_settings.save_path+city_name)
                with open(file_name, 'wb') as f:
                    f.write(res.content)
                    print('作品{}已抓取完成并保存到本地。。。'.format(name))
            except Exception as e:
                print(e)
                print('保存失败！！！')
    except:
        pass
