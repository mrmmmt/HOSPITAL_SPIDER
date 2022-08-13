import pandas as pd
import re
from tqdm import tqdm
import os

from yixue_com_spider.spider import main as yixue_main


df = pd.read_excel('hospital_info.xlsx', dtype='str')
df['医院名称'] = [re.compile('[\u4e00-\u9fff]+').findall(x)[0] for x in df['医院名称']]
df = df.drop_duplicates(subset='医院名称')
df = df[df['FLAG']!='del']
count = 0

for i in df.index:
    if count >= 50000:
        break
    if df['FLAG'][i] != 'T':
        hospital_name = df['医院名称'][i]
        count += 1
        try:
            title, hospital_level, hospital_type, hospital_jingyingfangshi, hospital_zhongdiankeshi = yixue_main(hospital_name)
            df['医院名称'][i] = title
            df['经营方式'][i] = hospital_jingyingfangshi
            df['医院类型'][i] = hospital_type
            df['医院等级'][i] = hospital_level
            df['重点科室'][i] = hospital_zhongdiankeshi
            df['FLAG'][i] = 'T'
            # if title != hospital_name:
            #     print(hospital_name+'->'+title+'\n')
            #     flag = input('请选择：')
            #     if flag == '1':
            #         df['医院名称'][i] = hospital_name
            #     elif flag == '2':
            #         df['医院名称'][i] = title
            #     else:
            #         df['建院年份'][i] = '-'
            #         df['是否医保'][i] = '-'
            #         df['科室数量'][i] = '-'
            #         df['病床数量'][i] = '-'
            #         df['医护人数'][i] = '-'
            #         df['年门诊数'][i] = '-'
            #         df['医院简介'][i] = '-'
            #         df['医院设备'][i] = '-'
            #         df['所获荣誉'][i] = '-'
            print(count, hospital_name, 'success')
        except Exception as e:
            df['FLAG'][i] = 'e'
            # if str(e) == '未查询到结果':
            #     df['FLAG'][i] = 'del'
            print(count, hospital_name, e)
            
            
df.to_excel('hospital_info.xlsx', index=None)