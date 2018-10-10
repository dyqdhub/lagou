#!/bin/python
# -*- coding:utf-8 -*-

import re
import time
import requests
import pymysql
import pandas as pd
from lxml import etree



# 预览页请求头
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '37',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': '_ga=GA1.2.559043944.1538036574; user_trace_token=20180927162255-88d2d23b-c22e-11e8-a722-525400f775ce; LGUID=20180927162255-88d2d54a-c22e-11e8-a722-525400f775ce; index_location_city=%E5%8C%97%E4%BA%AC; JSESSIONID=ABAAABAAAFCAAEG8B3CB2FFE51E53FB14CA5AACA372A8EC; _gid=GA1.2.649318914.1539051486; fromsite="localhost:63342"; utm_source=""; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1538036574,1538184134,1539051486,1539064490; TG-TRACK-CODE=search_code; _gat=1; LGSID=20181009152018-c6458d88-cb93-11e8-bba2-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_python%25E5%25BC%2580%25E5%258F%2591%3Fcity%3D%25E5%258C%2597%25E4%25BA%25AC%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_python%25E5%25BC%2580%25E5%258F%2591%3Fcity%3D%25E5%258C%2597%25E4%25BA%25AC%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D; LGRID=20181009152754-d65c6bd1-cb94-11e8-ad49-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1539070074; SEARCH_ID=6d9d242c7b094ac29b3ebdd9a389e925',
    'Host': 'www.lagou.com',
    'Origin': 'https://www.lagou.com',
    'Referer': 'https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?labelWords=sug&fromSearch=true&suginput=%E7%88%AC%E8%99%AB',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
    'X-Anit-Forge-Code': '0',
    'X-Anit-Forge-Token': 'None',
    'X-Requested-With': 'XMLHttpRequest',
    }

#职位详情页请求头
position_header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': '_ga=GA1.2.559043944.1538036574; user_trace_token=20180927162255-88d2d23b-c22e-11e8-a722-525400f775ce; LGUID=20180927162255-88d2d54a-c22e-11e8-a722-525400f775ce; index_location_city=%E5%8C%97%E4%BA%AC; JSESSIONID=ABAAABAAAFCAAEG8B3CB2FFE51E53FB14CA5AACA372A8EC; _gid=GA1.2.649318914.1539051486; fromsite="localhost:63342"; utm_source=""; PRE_UTM=; X_HTTP_TOKEN=34780b0c0c1917181ebdc30d92350f03; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216657c8a5a33a-0b0c8496c1843-5701631-1049088-16657c8a5a4d6%22%2C%22%24device_id%22%3A%2216657c8a5a33a-0b0c8496c1843-5701631-1049088-16657c8a5a4d6%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; sm_auth_id=bkn547rttjk1cagt; _gat=1; LGSID=20181009154444-2ff944bc-cb97-11e8-bba2-5254005c3644; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DMcm1YFv9J9_oAJP_JLABmIabagZbFlgy0hHLNZvTpSG%26wd%3D%26eqid%3D98cd5d7d000041a4000000025bbc5c69; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1538184134,1539051486,1539064490,1539071084; TG-TRACK-CODE=index_search; SEARCH_ID=ee4b5be634f54115af2c9de295210d89; LGRID=20181009154659-80edac5d-cb97-11e8-ad55-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1539071220',
    'Host': 'www.lagou.com',
    'Referer': 'https://www.lagou.com/jobs/list_python%E7%88%AC%E8%99%AB?labelWords=&fromSearch=true&suginput=',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
}

# 职业信息
position_info_dict = {
    'positionName':'',
    'salary':'',
    'city':'',
    'experience':'',
    'education':'',
    'describe':'',
    'workAdderss':'',
    'conpany':'',
    'territory':'',
    'phases':'',
    'scale':'',
}



# 保存到本地文件
'''
def save_locale(v_list):
    df = pd.DataFrame(v_list)
    df.to_excel('position.xlsx')
'''


#获取职位信息（本地保存部分）
'''
position_info_list = []
def get_position_info(position_url):
    response = requests.get(position_url,headers=position_header).text
    r_xml = etree.HTML(response)
    position_info_list.append(r_xml.xpath('//div[@class="job-name"]/span/text()')[0])
    value1 = r_xml.xpath('//dd[@class="job_request"]/p')
    info_p = value1[0].xpath('string(.)')
    position_info_list.append(info_p)      #这里要特别说明下：string()函数的使用我目前还不能和xpath语句连接到一起使用，这的使用方法是先将包含文本的标签定义为一个变量，然后再通过变量使用string函数得到所有文本内容。
    value2 = r_xml.xpath('//dd[@class="job_bt"]/div')
    position_info_list.append(value2[0].xpath('string(.)'))
    position_info_list.append(r_xml.xpath('//dl[@class="job_company"]/dt/a/img/@alt')[0])
    time.sleep(1)
'''



#写入数据库
def insertTab():
    #创建链接
    mysql_config = {
        'host':'192.168.29.129',
        'port':3306,
        'user':'spiderman',
        'passwd':'nihao123!',
        'db':'spider_1',
        'charset': 'utf8'
    }
    conn = pymysql.connect(**mysql_config)
    cursor = conn.cursor()
    sql = "INSERT INTO lagou(positionName,salary,city,experience,education,des,workAdderss,conpany,territory,phases,scale) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (position_info_dict["positionName"],position_info_dict["salary"],position_info_dict["city"],position_info_dict["experience"],position_info_dict["education"],position_info_dict["describe"],position_info_dict["workAdderss"],position_info_dict["conpany"],position_info_dict["territory"],position_info_dict["phases"],position_info_dict["scale"])
    # 插入数据的时候要事先创建好表个，列名不能与数据库函数冲突
    effect_row = cursor.execute(sql)
    # 保存数据
    conn.commit()
    #关闭游标
    cursor.close()
    # 断开连接
    conn.close()


#获取职位信息(入库部分)
def get_position_info(position_url):
    # 获取职位详情页
    position_html = requests.get(position_url,headers=position_header).text
    re_xml = etree.HTML(position_html)
    #获得职位名称并写入字典
    positionName = re_xml.xpath('//div[@class="job-name"]/span/text()')
    position_info_dict['positionName'] = positionName[0]
    #获得岗位工资并写入字典
    salary = re_xml.xpath('//div[@class="position-content-l"]/dd/p/span[1]/text()')
    position_info_dict['salary'] = salary[0]
    #获得城市并加入地名
    city = re_xml.xpath('//div[@class="position-content-l"]/dd/p/span[2]/text()')
    position_info_dict['city'] = city[0]
    #获得经验并加入字典
    experience = re_xml.xpath('//div[@class="position-content-l"]/dd/p/span[3]/text()')
    position_info_dict['experience'] = experience[0]
    #获得学历
    education = re_xml.xpath('//div[@class="position-content-l"]/dd/p/span[4]/text()')
    position_info_dict['education'] = education[0]
    # 获得职位描述
    describe = re_xml.xpath('//dd[@class="job_bt"]/div')
    describe_str = describe[0].xpath('string(.)').strip()
    position_info_dict['describe'] = describe_str
     #获得工作地点
    workAdderss = re_xml.xpath('//div[@class="work_addr"]/text()')
    position_info_dict['workAdderss'] = workAdderss[2]
    #获得公司名称
    conpany = re_xml.xpath('//dl[@class="job_company"]/dt/a/div/h2/text()')
    position_info_dict["conpany"] = conpany[0]
    #获得公司领域
    territory = re_xml.xpath('//dl[@id = "job_company"]/dd/ul/li[1]/text()')
    position_info_dict['territory'] = territory[1]
    phases = re_xml.xpath('//dl[@id = "job_company"]/dd/ul/li[2]/text()')
    position_info_dict['phases'] = phases[1]
    scale = re_xml.xpath('//dl[@id = "job_company"]/dd/ul/li[4]/text()')
    position_info_dict['scale'] = scale[1]
    #去除所有元素的空格和特殊字符
    for key in position_info_dict:
        position_info_dict[key] = position_info_dict[key].replace(' ','')
        position_info_dict[key] = re.sub('[\xa0/\n]','',position_info_dict[key])
        position_info_dict[key] = position_info_dict[key].replace('?','')
    insertTab()
    time.sleep(1)



# 获取预览页信息
def position_info(position_name,page_number):
    page_n = 1
    while page_n <= page_number:
        print("正在爬取第%s页" % page_n)
        #请求数据：first第一页为true时为第一页，pn表示第几页，kd表示职位名称
        from_data = {
            'first': 'true',
            'pn': page_n,
            'kd': position_name,
        }
        url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false'

        #获取职位预览页面数据
        rs = requests.post(url,data=from_data,headers=headers).json()
        #解析返回数据，获得职位ID，拼接成职位详情页
        result_dict = rs["content"]["positionResult"]["result"]
        for item in result_dict:
            positionId = str(item["positionId"])
            pra_url = 'https://www.lagou.com/jobs/' + positionId + '.html'
            # 获取职位详细信息（联众保存方式用的获取详情函数名称一样但内容不同，更改保存方式直接将不用的方式注释掉）
            get_position_info(pra_url)
            time.sleep(2)
        page_n += 1
    #保存文件到本地
    #save_locale(position_info_list)


if __name__ == "__main__":
    position_info("爬虫工程师",5)
