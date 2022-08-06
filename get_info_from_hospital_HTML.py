import re
from bs4 import BeautifulSoup
import os
from tqdm import tqdm
import time


root = './hospital_html'
file_lst = os.listdir(root)
for i, file in enumerate(file_lst):
    filename = root + '/' + file 
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'lxml')

    hospital_name = re.findall(r'<h1>(.+?)</h1>', html)
    if len(hospital_name) != 1:
        raise UserWarning('正则医院名不是一个结果')
    else:
        hospital_name = hospital_name[0]

    hospital_level = re.findall(r'<span class="grade">(.+?)</span>', html)
    if len(hospital_level) != 1:
        raise UserWarning('正则医院等级不是一个结果')
    else:
        hospital_level = hospital_level[0]

    hospital_type = re.findall(r'<p>性质：(.+?)</p>', html)
    if len(hospital_type) != 1:
        raise UserWarning('正则医院性质不是一个结果')
    else:
        hospital_type = hospital_type[0]

    table_soup = soup.find_all('table', {'class': 'present-table'})  # 医院信息表格
    if len(table_soup) != 1:
        raise UserWarning('soup医院表格不是一个结果')
    else:
        table_soup = str(table_soup[0])

    hospital_area = re.findall(r'<td><span>所在地区</span></td>.+?<td><.+?>(.+?)</a></td>', table_soup, re.S)[0]
    hospital_buildYear = re.findall(r'<td><span>建院年份</span></td>.+?<td><span>(.+?)</span></td>', table_soup, re.S)[0]
    hospital_roomNum = re.findall(r'<td><span>科室数量</span></td>.+?<td><span>(.+?)</span></td>', table_soup, re.S)[0]
    hospital_peopleNum = re.findall(r'<td><span>医护人数</span></td>.+?<td><span>(.+?)</span></td>', table_soup, re.S)[0]
    hospital_bedNum = re.findall(r'<td><span>病床数量</span></td>.+?<td><span>(.+?)</span></td>', table_soup, re.S)[0]
    hospital_caseNum = re.findall(r'<td><span>年门诊量</span></td>.+?<td><span>(.+?)</span></td>', table_soup, re.S)[0]
    hospital_isYIBAO = re.findall(r'<td><span>是否医保</span></td>.+?<td><span>(.+?)</span></td>', table_soup, re.S)[0]

    ## 简介
    try:
        intro_soup = soup.find_all('div', {'id': 'txtintro'})[0]
        hospital_intro = intro_soup.p.text.strip()
    except:
        hospital_intro = '未查询到'

    ## 设备
    try:
        equip_soup = soup.find_all('div', {'class': 'present-wrap2'})[0]
        hospital_intro = intro_soup.p.text.strip()
    except:
        hospital_intro = '未查询到'

    print(i, hospital_level)