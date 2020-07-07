import requests
from lxml import etree
import csv
import os
from bs4 import BeautifulSoup
import pandas as pd
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def is_valid(start,real,end):
    s=datetime.datetime.strptime(start[:-5],'%Y-%m-%d %H:%M:%S')
    r = datetime.datetime.strptime(real[:-5], '%Y-%m-%d %H:%M:%S')
    e = datetime.datetime.strptime(end[:-5], '%Y-%m-%d %H:%M:%S')

    #2020-06-07 21:00:00+0900
    #2020-06-07 23:30:00+0900
    return s<=r and r<=e

def get_records(contest_name,page_Nums):
    # 1 获取表头
    fields=["submit_time","task","user","score","status"]

    # 2 获取比赛开始结束时间
    print('比赛时间')
    url = "https://atcoder.jp/contests/" + contest_name
    r = requests.get(url, headers={
        "User-Agent": "Mozilla//5.0 (Windows NT 10.0; Win64; x64) AppleWebKit//537.36 (KHTML, like Gecko) Chrome//80.0.3987.132 Safari//537.36"})
    print(r.status_code)
    html = r.content.decode(r.encoding)
    # html = etree.HTML(html)
    # start_time = html.xpath("//small[@class='contest-duration']/a[1]/time[@class='fixtime-full']/text()")
    # end_time=html.xpath("//small[@class='contest-duration']/a[2]/time[@class='fixtime-full']")
    soup = BeautifulSoup(html, 'html.parser')
    time = soup.small.find_all('time')
    print(time)
    start_time=time[0].get_text()
    end_time=time[1].get_text()
    print(start_time,end_time)

    # 3 获取每一页的提交记录
    print("提交记录")
    rows=[]
    for i in range(500,page_Nums):
    #for i in range(558,page_Nums):
        print()
        print('第',i+1,'页')

        url = "https://atcoder.jp/contests/" + contest_name + "/submissions?page="+str(i+1)
        # driver = webdriver.Chrome()
        # driver.get(url)
        r=requests.get(url, headers={"User-Agent": "Mozilla//5.0 (Windows NT 10.0; Win64; x64) AppleWebKit//537.36 (KHTML, like Gecko) Chrome//80.0.3987.132 Safari//537.36"})
        print(r.status_code)
        html=r.content.decode(r.encoding)

        # 3.1 获取每页所有行的提交时间
        soup = BeautifulSoup(html, 'html.parser')
        tmp_time=soup.tbody.find_all('time') #[<time class="fixtime fixtime-second">2020-07-02 12:17:50+0900</time>, <time class="fixtime fixtime-second">2020-07-02 12:12:31+0900</time>]
        row_Nums=len(tmp_time)
        print('每页记录条数',row_Nums) #除了最后一页，应该都是20
        print('提交时间<time>tag', tmp_time)
        valid_idx=[]
        submit_time=[]
        for i in range(row_Nums):
            if is_valid(start_time,tmp_time[i].get_text(),end_time):
                valid_idx.append(i)
            submit_time.append(tmp_time[i].get_text())
        print(submit_time)

        # 3.2 获取其他提交记录的数据
        html=etree.HTML(html)
        for j in range(row_Nums):
            if j not in valid_idx:
                continue
            print('第',j+1,'行')
            row = []
            # ret=html.xpath("//tbody/tr["+str(j+1)+"]/td[@class='no-break']/time[@class='fixtime-second']/text()")#submit_time
            # row.append(ret)
            # element=WebDriverWait(driver,20).until(EC.element_to_be_clickable(()))
            row.append(submit_time[j]) #submit_time
            ret=html.xpath("//tbody/tr["+str(j+1)+"]/td[2]/a/text()")#task
            row.append(ret[0])
            ret=html.xpath("//tbody/tr["+str(j+1)+"]/td[3]/a[1]/text()")#user
            row.append(ret[0])
            ret=html.xpath("//tbody/tr["+str(j+1)+"]/td[@class='text-right submission-score']/text()")#score
            row.append(ret[0])
            ret=html.xpath("//tbody/tr["+str(j+1)+"]/td[@class='text-center'][1]/span/text()")#status
            row.append(ret[0])
            print(row)
            rows.append(row)
    filename = "contests\\"+contest_name + "\\record_"+contest_name+".csv"
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)


def exp():
    text = ''' <div> <ul> 
                <li class="item-1"><a href="link1.html">first item</a></li> 
                <li class="item-1"><a href="link2.html">second item</a></li> 
                <li class="item-inactive"><a href="link3.html">third item</a></li> 
                <li class="item-1"><a href="link4.html">fourth item</a></li> 
                <li class="item-0"><a href="link5.html">fifth item</a> 
                </ul> </div> '''
    html = etree.HTML(text)
    print(html) # <Element html at 0x1f1007c9d08>
    print(etree.tostring(html).decode())
    # 获取 class 为 item-1 li 下的 a 的 href
    ret1 = html.xpath('//li[@class="item-1"]/a/@href')
    print(ret1)
    # 获取 class 为 item-1 li 下的文本
    ret2 = html.xpath("//li[@class='item-1']/a/text()")
    print(ret2)


if __name__=="__main__":

    #get_records("agc045",326)
    #get_records("agc036", 912)
    #data = pd.read_csv("chosen_page_Nums.csv")
    #print(data)

    # for row in data.iterrows():
    #     print()
    #     # if row[1]['id']=='agc045' or row[1]['id']=='agc030' or row[1]['id']=='agc044':
    #     #     continue
    #     print(row[1])
    #     print(row[1]['id'])
    #     print(row[1]['page_Nums'])
    #     get_records(row[1]['id'],int(row[1]['page_Nums']))

    get_records('agc009',673)