import json
import re


with open('./data/yyk_99_province.html', 'r', encoding='utf-8') as f:
    html = f.read()

info_dict = dict()
areas_info = re.findall(r'<li>.+?</li>', html, re.S)
for i in range(len(areas_info)):
    area_info = areas_info[i]
    area = re.findall(r'class="aere-txt">(.+?)：</a>', area_info, re.S)[0]
    if area == '港澳台':
        continue
    print(area)
    temp_lst = list()
    province_info = re.findall(r'class="aere-txt2">(.+?)</a>', area_info)
    for j in range(len(province_info)):
        province = province_info[j]
        print(province)
        href = re.findall(r'<a href="(.+?)" target="_blank" title="'+province+'" class="aere-txt2">', area_info)[0]
        temp_lst.append({'province': province, 'href': href})
        print(province, href)
    info_dict[area] = temp_lst

with open('yyk_99_info.json', 'w', encoding='utf-8') as f:
    json.dump(info_dict, f)