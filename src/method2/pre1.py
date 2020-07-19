import requests
from lxml import etree
import csv
import os
import math
import pandas as pd
from pandas import DataFrame
from pandas import Series

'''
    选出合适的比赛
    将选出的比赛的题目ID和分数写进contests文件下对应的比赛文件夹中
'''




def process_id(rows,contest_name):   #爬下来的数据只有字母，该函数加上题号，如F ->  agc004_F
    for lst in rows:
        lst[0]=contest_name+lst[0][0]
    print('新的ID,eg.  agc004_F')
    print(rows)
    return rows

def check_validation(rows):  #有些比赛一题有两问，处理起来比较麻烦，则不取这些比赛
    for lst in rows:
        if '(' in lst[1]:
            return False
    return True

def get_difficulty(contest_name):
    url="https://atcoder.jp/contests/"+contest_name
    try:
        r=requests.get(url,headers = {"User-Agent": "Mozilla//5.0 (Windows NT 10.0; Win64; x64) AppleWebKit//537.36 (KHTML, like Gecko) Chrome//80.0.3987.132 Safari//537.36"})
        print(r.status_code) #状态码
    except Exception as e:
        print(contest_name,'爬取这次比赛的题目难度失败，可能是这场比赛不存在',e)
        return False
    html=r.content.decode(r.encoding)  #内容,字符串？
    html=etree.HTML(html)   #转换成HTML格式？
    #print(etree.tostring(html).decode())
    #ret=html.xpath('//table[@class="table table-responsible table-striped table-bordered"]/tbody/tr/td/text()')
    #ret=html.xpath("/html/body/div[@id='main-div']/div[@id='main-container']/div[@class='row']/div[@class='col-sm-12']/div[@id='contest-statement']/span[@class='lang']/span[@class='lang-en']/span[@class='lang-en']/div[@class='row']/div[@class='span4']/table[@class='table table-responsible table-striped table-bordered']/tbody/tr[1]/td[1]")
    ret=html.xpath("//div[@class='span4']/table[@class='table table-responsible table-striped table-bordered']/tbody/tr/td/text()")
    print(ret)  #为列表
    rows=[]
    for i in range(0,len(ret)//2,2):
        row=[]
        row.append(ret[i])
        row.append(ret[i+1])
        rows.append(row)
    print('爬取下来的分好组的题目分值')
    print(rows) #分好组的列表
    if not check_validation(rows):
        return False
    rows=process_id(rows,contest_name)
    if not os.path.exists("contests\\" + contest_name):
        os.mkdir("contests\\" + contest_name)
    filename = "contests\\"+contest_name+"\\score_"+contest_name+".csv"
    fields=['id','score']
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)
    return True



if __name__=="__main__":
    contests=[]
    for i in range(1,10):   #001-009
        contests.append("agc00"+str(i))
    for i in range(10,47):
        if i==42: continue #042没有这场比赛
        contests.append("agc0"+str(i))  #010-041 043-046

    chosen_contests=[]
    #获取题目难度，如果不带括号，则加入chosen_contests中，并且新建contests\\agc004\\score_agc004.csv，属性为id(带比赛的编号),score
    for contest_name in contests:
        print()
        if get_difficulty(contest_name):
            #每场比赛6题，但是比赛期间提交记录最多可上万，所以尽可能选取提交记录较少的比赛，同时选取每道题分值均固定的比赛
            chosen_contests.append(chosen_contests)
        else:
            print(contest_name+'不符合条件')
    print(chosen_contests)
