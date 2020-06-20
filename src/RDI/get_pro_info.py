import json

#      ***********!修改!字典类型case中的键值对**************
def init(case):
    case["record_Nums"] = 0
    case["AC_Nums"] = 0
    case["1A_Nums"] = 0
    case["total_Nums_before_AC"] = 0
    case["total_score"] = 0
    case["total_time_span"] = 0
    case["Nums_lower_70"] = 0


f=open("mini_record_lst.json",encoding="utf8")
res=f.read()
record_lst=json.loads(res)

f=open("mini_pro_dict.json",encoding="utf8")
res=f.read()
pro_dict=json.loads(res)


for inner_dict in pro_dict.values():
    init(inner_dict)

for record in record_lst:
    if record["is_TO"]:
        continue
    case=pro_dict[record["case_id"]]

    case["record_Nums"]+=1
    case["total_score"]+=record["final_score"]
    case["total_time_span"]+=record["time_span"]
    if int(record["final_score"])==100:
        case["AC_Nums"]+=1
        if record["is_1A"]:
            case["1A_Nums"]+=1
        else:
            case["total_Nums_before_AC"]+=record["Nums_before_AC"]
    elif int(record["final_score"])<70:
        case["Nums_lower_70"]+=1
        case["total_Nums_before_AC"]+=record["Nums_before_AC"]
    else:
        case["total_Nums_before_AC"]+=record["Nums_before_AC"]
    #pro_dict[record["case_id"]]=case    #不需要写回去


for v in pro_dict.values():
    #还有v["testCase_Nums"]也对RDI有影响
    try:
        v["AC_rate"]=v["AC_Nums"]/(v["total_Nums_before_AC"]+v["AC_Nums"])*100
    except ZeroDivisionError as e:  #不能写except Exception as e:
        print(v["case_id"],v["case_type"],v["case_name"])
        print('总AC次数为0',v["total_Nums_before_AC"],v["AC_Nums"],e)
    try:
        v["1A_rate"]=v["1A_Nums"]/v["record_Nums"]*100
        v["avg_score"]=v["total_score"]/v["record_Nums"]
        v["avg_time_span"]=v["total_time_span"]/v["record_Nums"]
        v["lower_70_rate"]=v["Nums_lower_70"]/v["record_Nums"]*100
    except ZeroDivisionError as e:
        print(v["case_id"], v["case_type"], v["case_name"])
        print('总提交次数为0，说明全都TO',v["record_Nums"],e)

json_pro=json.dumps(pro_dict,ensure_ascii=False, indent=4, separators=(',', ': '))
#要加encoding="utf8" 否则输出到.json中中文乱码
with open('mini_pro_detail_dict.json',mode='w',encoding="utf8") as f:
    f.write(json_pro)