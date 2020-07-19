import json

'''
fix

如果d_difficulty_dict.json的题目难度划分有变化，
可以运行此文件，
得到d_difficulty_dict_with_metrics_2.json

同时d_difficulty_dict_with_metrics_2.json比d_difficulty_dict_with_metrics.json多一个“平均分”字段，
以便绘制散点图，直观反应软件度量与平均分的关系
'''

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

