import json
import matplotlib.pyplot as plt

def draw(pro_dict):
    scores=[]#1准备数据
    for v in pro_dict.values():
        scores.append(v["avg_score"])
    plt.figure(figsize=(20,8),dpi=100)#2创建画布
    #3绘制直方图
    dist=4
    group_num=int((max(scores)-min(scores))/dist)
    plt.hist(scores,bins=group_num)
    plt.xticks(range(int(min(scores)),int(max(scores)+1),dist))#修改x轴刻度
    plt.grid(linestyle="--",alpha=0.5)#添加网格
    plt.xlabel("题目均分")#添加XY轴的描述信息
    plt.ylabel("题目数量")
    plt.show()#4显示图像

#x<60 C
#60<=x<88 B
#88<=x<100 A

def get_diff_level(pro_dict):
    difficulty_dict={}
    for v in pro_dict.values():
        inner_dict={}
        inner_dict["case_id"]=v["case_id"]
        inner_dict["case_type"]=v["case_type"]
        if v["avg_score"]<35:
            inner_dict["RDI"]="D"
        elif 35<=v["avg_score"] and v["avg_score"]<60:
            inner_dict["RDI"]="C"
        elif 60<= v["avg_score"] and v["avg_score"]<80:
            inner_dict["RDI"]="B"
        else:
            inner_dict['RDI']='A'
        difficulty_dict[v["case_id"]]=inner_dict

    json_pro=json.dumps(difficulty_dict,ensure_ascii=False, indent=4, separators=(',', ': '))
    # 要加encoding="utf8" 否则输出到.json中中文乱码
    with open('d_difficulty_dict.json',mode='w',encoding="utf8") as f:
        f.write(json_pro)
    with open('../PDI/d_difficulty_dict.json',mode='w',encoding="utf8") as f:
        f.write(json_pro)
    return difficulty_dict

def get_cnt(difficulty_dict):
    level_name=["A","B","C",'D']
    cnt=[0,0,0,0]
    for v in difficulty_dict.values():
        if v["RDI"]=="A":
            cnt[0]+=1
        elif v["RDI"]=="B":
            cnt[1]+=1
        elif v["RDI"]=="C":
            cnt[2]+=1
        else:
            cnt[3]+=1
    plt.figure(figsize=(20,8),dpi=80)
    plt.pie(cnt,labels=level_name,autopct="%1.2f%%")
    plt.legend()#显示图例
    plt.axis('equal')
    plt.show()

if __name__=='__main__':
    f = open("d_pro_detail_dict.json", encoding="utf8")
    res = f.read()
    pro_dict = json.loads(res)
    draw(pro_dict)
    difficulty_dict=get_diff_level(pro_dict)
    get_cnt(difficulty_dict)