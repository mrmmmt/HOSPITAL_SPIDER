# 得到所有医院的href
# 以得到医院url

import requests
import json
from bs4 import BeautifulSoup


def get_1_province_cities(href):
    """请求得到 一个省份所有的城市
    """
    url = 'https://yyk.99.com.cn' + href
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'yyk.99.com.cn',
        'Referer': 'https://yyk.99.com.cn/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }

    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise UserWarning('status_code: {}'.format(r.status_code))
    html = r.text

    soup = BeautifulSoup(html)
    res = list()
    items_raw = soup.find_all('a', {'class': 'tipnav'})
    for item in items_raw:
        title = item.attrs['title']
        href = item.attrs['href']
        res.append({'city': title, 'href': href})

    return res


def get_cities():
    with open('yyk_99_info.json', 'r', encoding='utf-8') as f:
        yyk_99_info = json.load(f)
    for area in yyk_99_info.keys():
        for i in range(len(yyk_99_info[area])):
            province_info = yyk_99_info[area][i]
            href = province_info['href']
            province_info['cities'] = get_1_province_cities(href)
            yyk_99_info[area][i] = province_info
    with open('yyk_99_info.json', 'w', encoding='utf-8') as f:
        json.dump(yyk_99_info, f)


def get1city_hospital(href_province, href_city):
    url = 'https://yyk.99.com.cn' + href_city
    # print(url)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'yyk.99.com.cn',
        'Referer': 'https://yyk.99.com.cn'+href_province,
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }

    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise UserWarning('status_code: {}'.format(r.status_code))
    html = r.text

    soup = BeautifulSoup(html)
    items_raw = soup.find_all('div', {'class': 'm-table-2'})
    res = list()
    for item in items_raw:
        td_lst = item.find_all('td')
        if len(td_lst) > 0:
            for i in range(len(td_lst)):
                td = td_lst[i]
                a = td.find_all('a')[0]
                title = a.attrs['title']
                href = a.attrs['href']
                res.append({'hospital': title, 'href': href})
    return res


def get_hospitals():
    with open('yyk_99_info.json', 'r', encoding='utf-8') as f:
        yyk_99_info = json.load(f)
    for area in yyk_99_info.keys():
        for i in range(len(yyk_99_info[area])):
            href_province = yyk_99_info[area][i]['href']
            cities_info = yyk_99_info[area][i]['cities']
            for j in range(len(cities_info)):
                city_info = yyk_99_info[area][i]['cities'][j]
                href_city = yyk_99_info[area][i]['cities'][j]['href']
                city_info['hospitals'] = get1city_hospital(href_province, href_city)
                yyk_99_info[area][i]['cities'][j] = city_info
                print(href_province, href_city, 'succ')

    with open('yyk_99_info.json', 'w', encoding='utf-8') as f:
        json.dump(yyk_99_info, f)


if __name__ == '__main__':
    # get_cities()
    # get_hospitals()
    with open('yyk_99_info.json', 'r', encoding='utf-8') as f:
        yyk_99_info = json.load(f)

