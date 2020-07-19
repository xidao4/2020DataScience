import requests
from lxml import etree
import csv
import datetime
from bs4 import BeautifulSoup

'''
爬下比赛时间内的所有提交记录
形成pro_with_features.csv
'''

def is_valid(start,real,end):
    s=datetime.datetime.strptime(start[:-5],'%Y-%m-%d %H:%M:%S')
    r = datetime.datetime.strptime(real[:-5], '%Y-%m-%d %H:%M:%S')
    e = datetime.datetime.strptime(end[:-5], '%Y-%m-%d %H:%M:%S')

    #2020-06-07 21:00:00+0900
    #2020-06-07 23:30:00+0900
    return s<=r and r<=e

def get_time_and_pages(contest_name):
    print('比赛时间')
    url = "https://atcoder.jp/contests/" + contest_name+'/submissions'
    r = requests.get(url, headers={
        "User-Agent": "Mozilla//5.0 (Windows NT 10.0; Win64; x64) AppleWebKit//537.36 (KHTML, like Gecko) Chrome//80.0.3987.132 Safari//537.36"})
    html = r.content.decode(r.encoding)
    # html = etree.HTML(html)
    # start_time = html.xpath("//small[@class='contest-duration']/a[1]/time[@class='fixtime-full']/text()")
    # end_time=html.xpath("//small[@class='contest-duration']/a[2]/time[@class='fixtime-full']")
    soup = BeautifulSoup(html, 'html.parser')
    time = soup.small.find_all('time')
    #print(time)
    start_time = time[0].get_text()
    end_time = time[1].get_text()
    # print(start_time, end_time)
    html=etree.HTML(html) #后一个html为str
    page_Nums = html.xpath("//div[@class='col-sm-12'][2]/div[@class='text-center'][1]/ul[@class='pagination pagination-sm mt-0 mb-1']/li[last()]/a/text()")
    page_Nums = int(page_Nums[0])
    #print(contest_name, '总页数', page_Nums)
    print('start_time',start_time)
    print('end_time',end_time)
    print('page_Nums',page_Nums)
    return start_time,end_time,page_Nums

def get_all_records(start_page_Num,page_Nums,start_time,end_time):
    rows=[]
    #从start_page_Num页开始，一直到最后一页
    for i in range(start_page_Num,page_Nums):
        print()
        #这一页
        print('第',i+1,'页')
        url = "https://atcoder.jp/contests/" + contest_name + "/submissions?page="+str(i+1)
        # driver = webdriver.Chrome()
        # driver.get(url)
        r=requests.get(url, headers={"User-Agent": "Mozilla//5.0 (Windows NT 10.0; Win64; x64) AppleWebKit//537.36 (KHTML, like Gecko) Chrome//80.0.3987.132 Safari//537.36"})
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
            #一页中的各个行
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
    return rows

def get_first_page(id):
    # 手动查看的
    if id=='003': return 1100
    if id=='006': return 788
    if id=='010': return 905
    if id=='013': return 820
    if id=='014': return 902
    if id=='015': return 802
    if id=='023': return 709
    if id=='024': return 763
    if id=='025': return 705
    if id=='029': return 1038
    if id=='031': return 571
    if id=='033': return 950
    if id == '034': return 950
    if id == '035': return 700
    if id == '038': return 611
    if id == '039': return 700
    if id == '043': return 400

def get_records(contest_name):
    #获取比赛开始和结束时间 以及 总页数
    start_time,end_time,page_Nums=get_time_and_pages(contest_name)
    #start_page_Num=get_start_page_Num(contest_name,page_Nums,start_time,end_time) #获取爬取的起始页数
    start_page_Num=get_first_page(contest_name[3:]) #获取开始爬取的页数
    #获取表头
    fields=["submit_time","task","user","score","status"]
    #获取每一场的提交记录
    rows=get_all_records(start_page_Num,page_Nums,start_time,end_time)
    #写进record_agc003.csv中
    filename = "contests\\"+contest_name + "\\record_"+contest_name+".csv"
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)

if __name__=='__main__':
    #pre1.py选取的比赛
    contests = [3, 6, 9, 10, 13, 14, 15, 16, 18, 23, 26, 32, 36, 37, 40, 44, 45, 46]
    for i in range(len(contests)):
        if len(str(contests[i])) == 1:
            contests[i] = 'agc00' + str(contests[i])
        else:
            contests[i] = 'agc0' + str(contests[i])

    for contest_name in contests:
        get_records(contest_name)