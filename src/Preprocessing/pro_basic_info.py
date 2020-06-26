import json
import numpy as np

#      ***********!修改!字典类型case中的键值对**************
def init(case):
    case["submit_Nums"] = 0
    case["total_time_span_to_AC"] = 0
    case["AC_Nums"] = 0
    case["1A_Nums"] = 0
    case["full_records"]=[]
    case["score_lst"]=[]


f=open("s_record_dict.json",encoding="utf8")
res=f.read()
record_dict=json.loads(res)

f=open("s_pro_dict.json",encoding="utf8")
res=f.read()
pro_dict=json.loads(res)


for inner_dict in pro_dict.values():
    init(inner_dict)

for record in record_dict.values():
    case = pro_dict[record["case_id"]]

    case["score_lst"].append(record["final_score"]) #均分算上非正常提交
    if record["is_1A"]:
        case["1A_Nums"]+=1
    if record["final_score"]==100:
        case["AC_Nums"]+=1
        case["total_time_span_to_AC"] += record["time_span"]
        if len(case["full_records"])==10: continue
        case["full_records"].append(record["path"])
    if record["is_py"] and not record["is_TO"]: #sumbit_Nums不算非正常提交
        case["submit_Nums"] += record["Nums_before_AC"]
        if record["final_score"]==100:
            case["submit_Nums"]+=1
    #pro_dict[record["case_id"]]=case    #不需要写回去


for v in pro_dict.values():
    #还有v["testCase_Nums"]也对RDI有影响
    try:
        v["AC_rate"]=v["AC_Nums"]/(v["submit_Nums"])*100    #sumbit_Nums不算非正常提交
        v["1A_rate"] = v["1A_Nums"] / v["AC_Nums"] * 100
        v["avg_time_span_to_AC"] = v["total_time_span_to_AC"] / v["AC_Nums"]
    except ZeroDivisionError as e:  #不能写except Exception as e:
        print(v["case_id"],v["case_type"],v["case_name"])
        print('提交总次数为0',v["submit_Nums"],e)
    try:
        v["avg_score"]=np.mean(v["score_lst"])      #均分算上非正常提交
        v["median"]=np.median(v["score_lst"])
    except ZeroDivisionError as e:
        print(v["case_id"], v["case_type"], v["case_name"])
        print('求取成绩平均数和中位数失败！',e)

json_pro=json.dumps(pro_dict,ensure_ascii=False, indent=4, separators=(',', ': '))
#要加encoding="utf8" 否则输出到.json中中文乱码
with open('s_pro_detail_dict.json',mode='w',encoding="utf8") as f:
    f.write(json_pro)