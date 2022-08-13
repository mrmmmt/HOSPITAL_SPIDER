import requests
from urllib import parse
from bs4 import BeautifulSoup
import re


def query_hospital_name_2_get_url(hospital_name):
    """查询医院名称
    得到查询到的第一条信息的url
    """
    url = 'https://www.yixue.com/index.php?title=%E7%89%B9%E6%AE%8A%3A%E6%90%9C%E7%B4%A2&search={}&fulltext=%E6%90%9C%E7%B4%A2%E8%AF%8D%E6%9D%A1'.format(parse.quote(hospital_name))
    headers = {
        # ':authority': 'www.yixue.com',
        # ':method': 'GET',
        # ':path': '/index.php?title=%E7%89%B9%E6%AE%8A%3A%E6%90%9C%E7%B4%A2&search={}&fulltext=%E6%90%9C%E7%B4%A2%E8%AF%8D%E6%9D%A1'.format(parse.quote(hospital_name)),
        # ':scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'referer': 'https://www.yixue.com/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }

    r = requests.get(url, headers=headers, timeout=10)
    if r.status_code != 200:
        raise UserWarning('status_code: {}'.format(r.status_code))
    html = r.text
    # with open('./yixue_com_html/demo.html', 'w', encoding='utf-8') as f:
    #     f.write(html)
    soup = BeautifulSoup(html, 'lxml')
    div_lst = soup.find_all('div', {'class': 'mw-search-result-heading'})
    if len(div_lst) == 0:
        return None, None
    div = div_lst[0]
    a = div.find_all('a')[0]
    title = a['title']
    href = a['href']
    return title, href


def req_hospital_page(title, href):
    url = 'https://www.yixue.com' + href
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }

    r = requests.get(url, headers=headers, timeout=10)
    if r.status_code != 200:
        raise UserWarning('status_code: {}'.format(r.status_code))
    html = r.text
    with open('./yixue_com_html/{}.html'.format(title), 'w', encoding='utf-8') as f:
        f.write(html)
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find_all('div', {'class': 'mw-parser-output'})[0]
    hospital_level = re.findall(r'<li><b>医院等级</b>：(.*?)</li>', str(div))[0]
    hospital_level = re.sub(r'<.+?>', '', hospital_level).strip()
    hospital_type = re.findall(r'<li><b>医院类型</b>：(.*?)</li>', str(div))[0]
    hospital_type = re.sub(r'<.+?>', '', hospital_type).strip()
    hospital_zhongdiankeshi = re.findall(r'<li><b>重点科室</b>：(.*?)</li>', str(div))[0]
    hospital_zhongdiankeshi = re.sub(r'<.+?>', '', hospital_zhongdiankeshi).strip()
    hospital_jingyingfangshi = re.findall(r'<li><b>经营方式</b>：(.*?)</li>', str(div))[0]
    hospital_jingyingfangshi = re.sub(r'<.+?>', '', hospital_jingyingfangshi).strip()

    return title, hospital_level, hospital_type, hospital_jingyingfangshi, hospital_zhongdiankeshi
    

def main(hospital_name):
    title, href = query_hospital_name_2_get_url(hospital_name)
    if href is None:
        raise UserWarning('未查询到结果')
    return req_hospital_page(title, href)


if __name__ == '__main__':
    hospital_name = '北京协和医院'
    # title, href = query_hospital_name_2_get_url(hospital_name)
    # req_hospital_page(title, href)
    main(hospital_name)