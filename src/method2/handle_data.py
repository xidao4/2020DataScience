import json
import csv
import pandas as pd

def handle_submit(contest_name):
    df=pd.read_csv("contests\\"+contest_name+"\\record_"+contest_name+".csv")
    d0={}
    for index,rows in df.iterrows():
        task=contest_name+"_"+rows['task'][0]   #eg. agc045_A
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

def get_pro_info(contest_name):
    return 0

if __name__=="__main__":
    handle_submit("agc045")
    get_pro_info("agc045")
