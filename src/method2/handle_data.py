import json
import csv
import pandas as pd
import datetime


def handle_submit(contest_name):
    df=pd.read_csv("contests\\"+contest_name+"\\record_"+contest_name+".csv")
    d0={}
    for index,rows in df.iterrows():
        task=contest_name+"_"+rows['task'][0]   #eg. agc028_F
        if task not in d0.keys():
            d0[task]={}
        d1=d0[task]
        user=rows['user']
        if user not in d1.keys():
            init_d2={'final_score':0,'upload_records':[]}
            d1[user]=init_d2
        d2=d1[user]
        score=rows['score']
        if score>d2['final_score']:
            d2['final_score']=score
        d3={'submit_time':rows['submit_time'],'status':rows['status'],'score':rows['score']}
        d2['upload_records'].append(d3)
    d0_json = json.dumps(d0, ensure_ascii=False, indent=4, separators=(',', ': '))
    with open("contests\\"+contest_name+"\\"+contest_name+"_handled.json", mode='w', encoding="utf8") as f:
        f.write(d0_json)

def get_interval(last,first):
    l = datetime.datetime.strptime(last[:-5], '%Y-%m-%d %H:%M:%S')
    f = datetime.datetime.strptime(first[:-5], '%Y-%m-%d %H:%M:%S')
    return (l-f).seconds

def add_new_cols():
    pros = pd.read_csv("pro.csv")
    pros = pros.set_index('id')
    print(pros)
    ac_rate_series = pd.Series([],dtype="float64")
    a1_rate_series = pd.Series([],dtype="float64")
    avg_ac_time_series = pd.Series([],dtype="float64")
    avg_score_series = pd.Series([],dtype="float64")
    pros.insert(2, 'ac_rate', ac_rate_series)
    pros.insert(3, '1a_rate', a1_rate_series)
    pros.insert(4, 'avg_ac_time', avg_ac_time_series)
    pros.insert(5, 'avg_score', avg_score_series)
    pros.insert(6,'score_rate',pd.Series([],dtype='float64'))
    pros.insert(7,'total_submit',pd.Series([],dtype="float64"))
    pros.insert(8,'ac_Nums',pd.Series([],dtype="float64"))
    pros.insert(9,'1a_Nums',pd.Series([],dtype='float64'))
    pros.insert(10,'ac_time',pd.Series([],dtype='float64'))
    pros.insert(11,'total_score',pd.Series([],dtype='float64'))
    pros.insert(12,'user_Nums',pd.Series([],dtype='float64'))
    print()
    print(pros)
    pros.to_csv("pro_with_features.csv")


def get_pro_info(contest_name):
    f=open("contests\\"+contest_name+"\\"+contest_name+"_handled.json")#encoding=utf8
    res = f.read()
    d0 = json.loads(res)

    pros=pd.read_csv("pro_with_features.csv")
    #print(pros)
    pros=pros.set_index('id')
    print(pros)

    for k0,v0 in d0.items():
        total_submit=0
        ac_Nums=0
        a1_Nums=0
        ac_time=0
        total_score=0
        user_Nums=len(v0)
        for k1,v1 in v0.items():
            total_score+=v1['final_score']/100
            submit_Nums=len(v1['upload_records'])
            total_submit+=submit_Nums
            upload_lst=v1['upload_records']
            for i in range(len(upload_lst)):
                if upload_lst[i]['status']=='AC':
                    ac_Nums+=1
                    if submit_Nums == 1:
                        a1_Nums+=1
                    ac_time+=get_interval(upload_lst[i]['submit_time'],upload_lst[-1]['submit_time'])
                    break

        try:
            ac_rate=ac_Nums/total_submit*100
            pros.at[k0, 'ac_rate'] = ac_rate
        except ZeroDivisionError as e:
            pros.at[k0, 'ac_rate'] = 0
            print(e)
        try:
            a1_rate=a1_Nums/ac_Nums*100
            pros.at[k0, '1a_rate'] = a1_rate
        except ZeroDivisionError as e:
            pros.at[k0, '1a_rate'] = 0
            print(e)
        try:
            avg_ac_time=ac_time/ac_Nums
            pros.at[k0, 'avg_ac_time'] = avg_ac_time
        except ZeroDivisionError as e:
            pros.at[k0, 'avg_ac_time'] = 0
            print(e)
        try:
            avg_score=total_score/user_Nums*100
            pros.at[k0, 'avg_score'] = avg_score
        except ZeroDivisionError as e:
            pros.at[k0, 'avg_score'] = 0
            print(e)

        pros.at[k0, 'score_rate'] =pros.at[k0,'avg_score']/pros.at[k0,'score']*100
        pros.at[k0,'total_submit']=total_submit
        pros.at[k0,'ac_Nums']=ac_Nums
        pros.at[k0,'1a_Nums']=a1_Nums
        pros.at[k0,'ac_time']=ac_time
        pros.at[k0,'total_score']=total_score
        pros.at[k0,'user_Nums']=user_Nums

    print(pros)
    pros.to_csv("pro_with_features.csv")

if __name__ == "__main__":
    handle_submit("agc036")
    #add_new_cols()
    get_pro_info("agc036")
