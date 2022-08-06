import os
import json
import requests
import time
from fake_useragent import UserAgent
from random import randint


def get1hospital_html(hospital_href, proxy=None):
    url = 'https://yyk.99.com.cn'+hospital_href+'jianjie.html'
    ua = UserAgent()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'yyk.99.com.cn',
        'Referer': 'https://yyk.99.com.cn'+hospital_href,
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': ua.random
    }

    # r = requests.get(url, headers=headers, timeout=10, proxies=proxy)
    r = requests.get(url, headers=headers, timeout=10, allow_redirects=False)  # 禁止重定向，不然出错
    if r.status_code != 200:
        raise UserWarning('status_code: {}'.format(r.status_code))
    html = r.text
    with open('./hospital_html/'+hospital_href.strip('/').replace('/', '-')+'.html', 'w', encoding='utf-8') as f:
        f.write(html)


def get_all_href_info():
    """得到所有的医院href信息，返回list
    list[i][0] = hospital name
    list[i][1] = hospital href
    """
    href_lst = list()
    with open('yyk_99_info.json', 'r', encoding='utf-8') as f:
        yyk_99_info = json.load(f)
    for area in yyk_99_info.keys():
        for i in range(len(yyk_99_info[area])):
            cities = yyk_99_info[area][i]['cities']
            for j in range(len(cities)):
                city = cities[j]
                hospitals = city['hospitals']
                for k in range(len(hospitals)):
                    hospital_name = hospitals[k]['hospital']
                    hospital_href = hospitals[k]['href']
                    href_lst.append([hospital_name, hospital_href])
   
    return href_lst
    

def build_need2req_json():
    """得到医院href的json
    包含所有的，已爬取的和未爬取的
    """
    if not os.path.exists('need2req.json'):
        all_hospital_info = get_all_href_info()
    else:
        with open('need2req.json', 'r', encoding='utf-8') as f:
            need2req = json.load(f)
        all_hospital_info = need2req['need2hospitals']
    
    need2hospitals = []
    for hospital_info in all_hospital_info:
        hospital_href = hospital_info[1]
        if hospital_href.strip('/').replace('/', '-')+'.html' not in already_files:
            need2hospitals.append(hospital_info)
    res = {
        'need2hospitals': need2hospitals
    }
    
    with open('need2req.json', 'w', encoding='utf-8') as f:
        json.dump(res, f)


def remainingTime(startTime_G, data_num, download_finish_count):
    """计算剩余时间"""
    timeSpent = time.time() - startTime_G
    timeRemaining = int(timeSpent * (data_num-download_finish_count) / download_finish_count)
    s = timeRemaining % 60
    m = (timeRemaining - s) % 3600 // 60
    h = (timeRemaining - s - m*60) // 3600
    return "{h}:{m}:{s}".format(h=h, m=str(m).zfill(2), s=str(s).zfill(2))



if __name__ == '__main__':
    root = './hospital_html'
    already_files = os.listdir(root)
    
    proxy = {
        'http': '101.200.127.149:3129'
    }

    build_need2req_json()
    with open('need2req.json', 'r', encoding='utf-8') as f:
        need2req = json.load(f)
    need2hospitals = need2req['need2hospitals']
            
    href_lst = list()
    for hospital_info in need2hospitals:
        hospital_href = hospital_info[1]
        href_lst.append(hospital_href)

    startTime_G = time.time()
    data_num = len(href_lst)
    for i, hospital_href in enumerate(href_lst):
        download_finish_count = i+1
        if hospital_href.strip('/').replace('/', '-')+'.html' not in already_files:
            try:
                # get1hospital_html(hospital_href, proxy)
                get1hospital_html(hospital_href)
                print('{0}/{1}'.format(download_finish_count, data_num), hospital_href, 'success', remainingTime(startTime_G, data_num, download_finish_count))
            except Exception as e:
                with open('error.txt', 'a', encoding='utf-8') as f:
                    f.write(hospital_href+'|'+str(e)+'\n')
                print('{0}/{1}'.format(download_finish_count, data_num), hospital_href, 'fail', remainingTime(startTime_G, data_num, download_finish_count))
            # finally:
            #     time.sleep(randint(1, 5))
        # else:
        #     print(hospital_href, 'success')
        