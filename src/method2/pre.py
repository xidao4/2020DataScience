import requests
from lxml import etree
import csv
import os
import math
import pandas as pd
from pandas import DataFrame
from pandas import Series


def get_page_Nums(contest_name,pages):
    url="https://atcoder.jp/contests/"+contest_name+"/submissions"
    #获取总页数
    r = requests.get(url, headers={"User-Agent": "Mozilla//5.0 (Windows NT 10.0; Win64; x64) AppleWebKit//537.36 (KHTML, like Gecko) Chrome//80.0.3987.132 Safari//537.36"})
    print(r.status_code)
    html = r.content.decode(r.encoding)
    html = etree.HTML(html)
    page_Nums=html.xpath("/html/body/div[@id='main-div']/div[@id='main-container']/div[@class='row']/div[@class='col-sm-12'][2]/div[@class='text-center'][1]/ul[@class='pagination pagination-sm mt-0 mb-1']/li[last()]/a/text()")
    page_Nums=int(page_Nums[0])
    print(page_Nums)
    pages[contest_name]=page_Nums

def get_total_page_Nums(contests):
    pages = {}
    for contest in contests:
        print(contest)
        get_page_Nums(contest,pages)
    s = Series(pages).sort_values()
    print(s)
    print(s.describe())
    s.to_csv("page_Nums.csv")

def get_chosen_page_Nums():
    data = pd.read_csv("page_Nums.csv")
    data.rename(columns={'Unnamed: 0':'id','0': 'page_Nums'},inplace=True)
    data=data.sort_values(by='page_Nums')
    data=data.iloc[:18,:2]
    print(data)
    data.to_csv("chosen_page_Nums.csv", index=False)

def get_score(score_str):
    idx=score_str.find('(')
    if idx==-1:
        return int(score_str)
    else:
        return int(score_str[:idx])

def str_to_int(arrLike):
    if isinstance(arrLike['score'],int):
        return arrLike['score']
    return get_score(arrLike['score'])

def get_new_id(arrLike,contest):
    id=arrLike['id']
    # idx = id.find(',')
    # if idx==-1:
    #     return contest+'_'+id
    # else:
    #     return contest+'_'+id[:idx]
    return contest+'_'+id

def get_difficulty(contest_name):

    print("OJ给的题目难度（由题目的分值决定）")
    url="https://atcoder.jp/contests/"+contest_name
    try:
        r=requests.get(url,headers = {"User-Agent": "Mozilla//5.0 (Windows NT 10.0; Win64; x64) AppleWebKit//537.36 (KHTML, like Gecko) Chrome//80.0.3987.132 Safari//537.36"})
        print(r.status_code) #状态码
    except Exception as e:
        print(contest_name,'爬取这次比赛的题目难度失败，可能是这场比赛不存在',e)
        return
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
    print('分好组的列表')
    print(rows) #分好组的列表
    filename = "contests\\"+contest_name+"\\pro_score.csv"
    fields=['id','score']
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)
    #获取modify_score,同时获取带比赛编号的题目名称id
    data = pd.read_csv(filename)
    print('变换前')
    print(data)
    #data['modify_score'] = data.apply(str_to_int, axis=1)
    data['id'] = data.apply(get_new_id, axis=1, args=(contest_name,))
    #del data['score']
    print('变换后')
    print(data)
    data.to_csv("contests\\" + contest_name + "\\pro_score_modify.csv", index=False)# id modify_score
    print()
    print()
    print()


def get_diff_lvl(arrLike):
    s=arrLike['score']
    if s<600: return 'A'
    elif s<1000: return 'B'
    elif s<1400: return 'C'
    else: return 'D'


def modify_id(arrLike):
    id=arrLike['id']
    idx = id.find(',')
    if idx == -1:
        return id
    else:
        return id[:idx]

def get_chosen_pro_info():
    data = pd.read_csv("chosen_page_Nums.csv")

    contest_series = data.id
    # for i, v in contest_series.items():
    #     id.append(v + '_A')
    #     id.append(v + '_B')
    #     id.append(v + '_C')
    #     id.append(v + '_D')
    #     id.append(v + '_E')
    #     id.append(v + '_F')
    # my_dict = {'id': id}
    # df = DataFrame(my_dict)
    df1=DataFrame({'id':[]})
    for i,v in contest_series.items():
        df2=pd.read_csv("contests\\"+v+"\\pro_score_modify.csv")
        df2['id']=df2.apply(modify_id,axis=1)
        df1=pd.merge(df1,df2,how='outer')
    print(df1)
    df1['difficulty_level']=df1.apply(get_diff_lvl,axis=1)
    df1=df1.set_index('id')
    print(df1)
    df1.to_csv("pro.csv",index=True)

if __name__=="__main__":
    contests=[]
    for i in range(1,10):   #001-009
        contests.append("agc00"+str(i))
    for i in range(10,47):
        if i==42: continue #042没有这场比赛
        contests.append("agc0"+str(i))  #010-041 043-046
    #get_total_page_Nums(contests)  #获取全部比赛的页数   page_Nums.csv
    #get_chosen_page_Nums()  #页数从小到大排序，获取前18场比赛      chosen_page_Nums.csv
    #选定的比赛的题目分数及相应难度
    data = pd.read_csv("chosen_page_Nums.csv")
    contest_series=data.id
    for i,contest in contest_series.items():
        print(contest)
        path="contests\\"+contest
        if not os.path.exists(path):
            os.mkdir(path)
        #选定的比赛的题目的分数
        #get_difficulty(contest) #选定的比赛的题目的难度
    get_chosen_pro_info()  #选定的比赛的题目id,modify_score,difficulty_level