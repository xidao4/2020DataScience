# 不要运行这个文件
"""
获取随机数组
list = random.sample(range(1, len(data)), 50)
将两个随机样本固定为 fifty_abnormal_sample.json 和 fifty_valid_sample.json
"""
"""
f = open("abnormal_dict.json", encoding="utf8")
res = f.read()
data = json.loads(res)
data = list(dict.values(data))

a_list = random.sample(range(1, len(data)), 50)
a_list.sort()

fifty_abnormal_dic = {}
i = -1
for record in data:
    i += 1
    if i in a_list:
        key = record["record_id"]
        fifty_abnormal_dic[key] = record

with open('fifty_abnormal_dict.json', 'w') as f:
    f.write(json.dumps(fifty_abnormal_dic, ensure_ascii=False, indent=4, separators=(',', ': ')))
print(len(fifty_abnormal_dic)) #50
"""

"""
f = open("valid_dict.json", encoding="utf8")
res = f.read()
data = json.loads(res)
data = list(dict.values(data))

v_list = random.sample(range(1, len(data)), 50)
v_list.sort()

fifty_valid_dic = {}
i = -1
for record in data:
    i += 1
    if i in v_list:
        key = record["record_id"]
        fifty_valid_dic[key] = record

with open('fifty_abnormal_dict.json', 'w') as f:
    f.write(json.dumps(fifty_valid_dic, ensure_ascii=False, indent=4, separators=(',', ': ')))
print(len(fifty_valid_dic))  #50
"""