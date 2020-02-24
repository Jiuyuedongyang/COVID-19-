import requests
import json
from bs4 import BeautifulSoup
import re
import datetime
import os
import time

while True:
    time_now = time.strftime("%H:%M:%S", time.localtime())  # 刷新
    if time_now == "22:00:00":  # 此处设置每天定时的时间
        
        
        
        
        
        
        
        starttime = time.time()
        
        url = 'https://ncov.dxy.cn/ncovh5/view/pneumonia'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
        r = requests.get(url, headers=headers)
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        
        get_data1 = soup.find_all('script', attrs={'id': 'getAreaStat'})
        get_data2 = get_data1[0].string
        RE = re.compile('\[.*\]')
        data_clear = re.findall(RE, get_data2)
        data_clear[0]  # 这里有个列表，我们去除第0个
        data_json = json.loads(data_clear[0])  # 将字典格式转换换为json格式
        Number_of_China_provinces = len(
            json.loads(data_clear[0]))  # 查看有几个省市，用于遍历。由常识可知，中华人民共和国有34个省级行政区域，包括23个省，5个自治区，4个直辖市，2个特别行政区。
        
        datetime.datetime.now()
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H：%M')
        
        isExist = os.path.exists(f'./{now_time}疫情数据信息')
        if not isExist:
            os.makedirs(f'./{now_time}疫情数据信息')
        else:
            pass
        # os.makedirs(f'./疫情数据信息')
        
        city_list = []
        for provinces in range(Number_of_China_provinces):
            file_name = data_json[provinces]['provinceName']
            name = f'./{now_time}疫情数据信息/{file_name}.csv'
            print(f'正在爬取{file_name}信息，请稍等...')
            with open(name, 'w', encoding='utf-8-sig')as f1:
                Number_of_this_Province_city = len(data_json[provinces]['cities'])
                provinceName = data_json[provinces]['provinceName']
                confirmedCount = data_json[provinces]['confirmedCount']
                deadCount = data_json[provinces]['deadCount']
                curedCount = data_json[provinces]['curedCount']
                
                f1.write(file_name)
                f1.write('\n')
                
                title = '{0},{1},{2},{3}'
                f1.write(title.format('地区', '确诊', '死亡', '治愈'))
                f1.write('\n')
                f1.write('所有地区合计')
                f1.write(',')
                f1.write(str(confirmedCount))
                f1.write(',')
                f1.write(str(deadCount))
                f1.write(',')
                f1.write(str(curedCount))
                f1.write('\n')
            
            for city in range(Number_of_this_Province_city):
                time.sleep(0.004)
                with open(name, 'a', encoding='utf-8-sig')as f2:
                    cityName = data_json[provinces]['cities'][city]['cityName']
                    confirmedCount = data_json[provinces]['cities'][city]['confirmedCount']
                    deadCount = data_json[provinces]['cities'][city]['deadCount']
                    curedCount = data_json[provinces]['cities'][city]['curedCount']
                    print(f'    正在爬取({cityName})信息，请稍等...')
                    f2.write(cityName)
                    f2.write(',')
                    
                    f2.write(str(confirmedCount))
                    f2.write(',')
                    
                    f2.write(str(deadCount))
                    f2.write(',')
                    
                    f2.write(str(curedCount))
                    f2.write(',')
                    f2.write('\n')
            print(f'爬取「{file_name}」成功！\n')
            #     print(f'爬取「{file_name}」成功！')
            with open(name, 'a', encoding='utf-8-sig')as f3:
                f3.write('信息爬取时间：' + now_time)
        endtime = time.time()
        elapsed_time = endtime - starttime
        print(f'\n------------------------------\n'
              f'所有（共计{provinces + 1}）个省份已经爬取完毕！\n'
              f'请前往文件夹查看，谢谢！\n'
              f'共耗时{elapsed_time:.6f}s'
              f'\n------------------------------ \n')
        # 爬取程序完成
        
        
        
        
        # 定时操作成功性测试打印
        print("定时操作成功性测试")
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 定时发送测试")
        
        time.sleep(100)  # 因为以秒定时，所以暂停2秒，使之不会在1秒内执行多次
