import re
from bs4 import BeautifulSoup
import os
from tqdm import tqdm
import json


root = './hospital_html'
file_lst = os.listdir(root)
with open('hospital_infos.json', 'r', encoding='utf-8') as f:
    info_dict = json.load(f)

# for file in tqdm(file_lst):
#     # if '80404' not in file:
#     #     continue
#     try:
#         filename = root + '/' + file 
#         with open(filename, 'r', encoding='utf-8') as f:
#             html = f.read()
#         soup = BeautifulSoup(html, 'lxml')

#         hospital_name = re.findall(r'<h1>(.+?)</h1>', html)[0]

#         hospital_level = re.findall(r'<span class="grade">(.+?)</span>', html)
#         if len(hospital_level) != 1:
#             raise UserWarning('正则医院等级不是一个结果')
#         else:
#             hospital_level = hospital_level[0]

#         hospital_type = re.findall(r'<p>性质：(.+?)</p>', html)
#         if len(hospital_type) != 1:
#             raise UserWarning('正则医院性质不是一个结果')
#         else:
#             hospital_type = hospital_type[0]

#         table_soup = soup.find_all('table', {'class': 'present-table'})  # 医院信息表格
#         if len(table_soup) != 1:
#             raise UserWarning('soup医院表格不是一个结果')
#         else:
#             table_soup = str(table_soup[0])

#         hospital_area = re.findall(r'<td><span>所在地区</span></td>.+?<td><a .+?>(.+?)</a></td>', table_soup, re.S)[0]
#         hospital_buildYear = re.findall(r'<td><span>建院年份</span></td>.+?<td><span>(.+?)</span></td>', table_soup, re.S)[0]
#         hospital_roomNum = re.findall(r'<td><span>科室数量</span></td>.+?<td><a .+?>(.+?)</a></td>', table_soup, re.S)[0]
#         hospital_peopleNum = re.findall(r'<td><span>医护人数</span></td>.+?<td><a .+?>(.+?)</a></td>', table_soup, re.S)[0]
#         hospital_bedNum = re.findall(r'<td><span>病床数量</span></td>.+?<td><span>(.+?)</span></td>', table_soup, re.S)[0]
#         hospital_caseNum = re.findall(r'<td><span>年门诊量</span></td>.+?<td><span>(.+?)</span></td>', table_soup, re.S)[0]
#         hospital_isYIBAO = re.findall(r'<td><span>是否医保</span></td>.+?<td><span>(.+?)</span></td>', table_soup, re.S)[0]

#         ## 简介
#         try:
#             temp_lst = list()
#             intro_soup = soup.find_all('div', {'class': 'present-wrap1'})[0]
#             intro_lst = re.findall(r'<p>(.*?)</p>', str(intro_soup), re.S)
#             for i in range(len(intro_lst)):
#                 if len(intro_lst[i]) != 0:
#                     temp_lst.append(intro_lst[i].strip())
#             hospital_intro = '\n'.join(temp_lst)
#         except:
#             hospital_intro = '未查询到'

#         ## 设备
#         try:
#             temp_lst = list()
#             equip_soup = soup.find_all('div', {'class': 'present-wrap2'})[0]
#             equip_lst = re.findall(r'<p>(.*?)</p>', str(equip_soup), re.S)
#             for i in range(len(equip_lst)):
#                 if len(equip_lst[i]) != 0:
#                     temp_lst.append(equip_lst[i].strip())
#             equip_intro = '\n'.join(temp_lst)
#         except:
#             equip_intro = '未查询到'

#         ## 所获荣誉
#         try:
#             temp_lst = list()
#             honor_soup = soup.find_all('div', {'class': 'present-wrap2 present-hx'})[0]
#             honor_lst = re.findall(r'<p>(.*?)</p>', str(honor_soup), re.S)
#             for i in range(len(honor_lst)):
#                 if len(honor_lst[i]) != 0:
#                     temp_lst.append(honor_lst[i].strip())
#             honor_intro = '\n'.join(temp_lst)
#         except:
#             honor_intro = '未查询到'

#         info_dict[file[:-5]] = {
#             'hospital_name': hospital_name,
#             'hospital_level': hospital_level,
#             'hospital_type': hospital_type,
#             'hospital_area': hospital_area,
#             'hospital_buildYear': hospital_buildYear,
#             'hospital_keshiNum': hospital_roomNum,
#             'hospital_yihuNum': hospital_peopleNum,
#             'hospital_bingchuangNum': hospital_bedNum,
#             'hospital_nianmenzhenNum': hospital_caseNum,
#             'hospital_isYIBAO': hospital_isYIBAO,
#             'hospital_intro': hospital_intro,
#             'equip_intro': equip_intro,
#             'honor_intro': honor_intro
#         }
#     except Exception as e:
#         with open('error.txt', 'a', encoding='utf-8') as f:
#             f.write('{0}|{1}\n'.format(file[:-5], str(e).strip()))

# with open('hospital_infos.json', 'w', encoding='utf-8') as f:
#     json.dump(info_dict, f)