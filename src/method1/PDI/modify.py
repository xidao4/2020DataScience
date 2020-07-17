import json

if __name__=='__main__':
    f=open('d_difficulty_dict_with_metrics.json',encoding="utf8")
    res=f.read()
    pre=json.loads(res)

    f = open("d_pro_detail_dict.json", encoding="utf8")
    res = f.read()
    score= json.loads(res)
    for k,v in score.items():
        pre[k]['avg_score']=v['avg_score']


    f=open('d_difficulty_dict.json',encoding='utf8')
    res=f.read()
    level=json.loads(res)
    for k,v in level.items():
        pre[k]['RDI']=v['RDI']

    json_pro=json.dumps(pre,ensure_ascii=False, indent=4, separators=(',', ': '))
    with open('d_difficulty_dict_with_metrics_2.json',mode='w',encoding="utf8") as f:
        f.write(json_pro)

