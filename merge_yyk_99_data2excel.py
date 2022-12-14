import json
from tqdm import tqdm
import os


with open('yyk_99_info.json', 'r', encoding='utf-8') as f:
    area_info = json.load(f)
    
with open('hospital_infos.json', 'r', encoding='utf-8') as f:
    hospital_infos = json.load(f)

for area in area_info.keys():
    print(area)
    province_lst = area_info[area]
    for i in tqdm(range(len(province_lst))):
        province = province_lst[i]['province']
        city_lst = province_lst[i]['cities']
        for j in range(len(city_lst)):
            city = city_lst[j]['city']
            hospital_lst = city_lst[j]['hospitals']
            for k in range(len(hospital_lst)):
                hospital_name = hospital_lst[k]['hospital']
                href = hospital_lst[k]['href'].strip('/').replace('/', '-')
                if href in hospital_infos.keys():
                    hospital_info = hospital_infos[href]
                    hospital_name = hospital_info['hospital_name']                  
                    hospital_type = hospital_info['hospital_type']
                    hospital_level = hospital_info['hospital_level']
                    hospital_area = hospital_info['hospital_area']
                    hospital_buildYear = hospital_info['hospital_buildYear']
                    hospital_isYIBAO = hospital_info['hospital_isYIBAO']
                    hospital_keshiNum = hospital_info['hospital_keshiNum']
                    hospital_bingchuangNum = hospital_info['hospital_bingchuangNum']
                    hospital_yihuNum = hospital_info['hospital_yihuNum']
                    hospital_nianmenzhenNum = hospital_info['hospital_nianmenzhenNum']
                    hospital_intro = hospital_info['hospital_intro'].strip().replace('\n', ' ')
                    equip_intro = hospital_info['equip_intro'].strip().replace('\n', ' ')
                    honor_intro = hospital_info['honor_intro'].strip().replace('\n', ' ')
                    
                else:
                    hospital_type = '-'
                    hospital_level = '-'
                    hospital_area = '-'
                    hospital_buildYear = '-'
                    hospital_isYIBAO = '-'
                    hospital_keshiNum = '-'
                    hospital_bingchuangNum = '-'
                    hospital_yihuNum = '-'
                    hospital_nianmenzhenNum = '-'
                    hospital_intro = '-'
                    equip_intro = '-'
                    honor_intro = '-'
                
                if not os.path.exists('./hospital_info.txt'):
                    with open('./hospital_info.txt', 'w', encoding='utf-8') as f:
                        f.write('??????|??????|??????|??????|????????????|'+
                                '????????????|????????????|????????????|????????????|'+
                                '????????????|????????????|????????????|????????????|'+
                                '????????????|????????????|????????????\n')
                with open('./hospital_info.txt', 'a', encoding='utf-8') as f:
                    f.write('{0}|{1}|{2}|{3}|{4}|{5}|{6}|{7}|{8}|{9}|{10}|{11}|{12}|{13}|{14}|{15}\n'.format(
                        area, province, city, hospital_area, hospital_name,
                        hospital_type, hospital_level, hospital_buildYear, hospital_isYIBAO,
                        hospital_keshiNum, hospital_bingchuangNum, hospital_yihuNum, hospital_nianmenzhenNum,
                        hospital_intro, equip_intro, honor_intro))
                