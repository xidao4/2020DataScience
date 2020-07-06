import json
import os
import random
f=open("s_pro_detail_dict.json",encoding="utf8")
res=f.read()
pro_dict=json.loads(res)
target=10  #随机选十份有用代码计算度量值

commands=[]
pre="metrics\\"
for v in pro_dict.values():
    if not os.path.exists(pre+v["case_id"]):
        os.mkdir(pre+v["case_id"])
    if not os.path.exists(pre+v["case_id"]+"\\cc"):
        os.mkdir(pre+v["case_id"]+"\\cc")
    if not os.path.exists(pre+v["case_id"]+"\\hal"):
        os.mkdir(pre+v["case_id"]+"\\hal")
    if not os.path.exists(pre+v["case_id"]+"\\LLOC"):
        os.mkdir(pre+v["case_id"]+"\\LLOC")
#新增
    usefulRecord=[]      #存放所有的有用的提交代码路径  包括参考答案和同学的满分答案
    for i in v["full_records"]:
        url = "E:\\2020DataScience\\src\\Preprocessing\\" + i + "main_modify.py"
        usefulRecord.append(url)
    if len(usefulRecord)>=target:
        usefulRecord=random.sample(usefulRecord,target)  #随机抽取target份
    if v["ans_is_py"]:
        if len(usefulRecord)==target:   #满足target个删掉一个让给标准答案
              usefulRecord=random.sample(usefulRecord,len(usefulRecord)-1)  #一定把是py的参考答案加进去
        url = "E:\\2020DataScience\\src\\Preprocessing\\" + v["case_unzip_dir"] + ".mooctest\\answer_modify.py"
        usefulRecord.append(url)
    if len(usefulRecord)==0:
        continue
    for u in usefulRecord:
        url=u
        output_url="E:\\2020DataScience\\src\\method1\\PDI\\metrics\\"+v["case_id"]+"\\cc\\cc"+str(usefulRecord.index(u))+".json"
        c="radon cc "+url+" --show-complexity --json --output-file \""+output_url+"\"\n"
        commands.append(c)
        output_url="E:\\2020DataScience\\src\\method1\\PDI\\metrics\\"+v["case_id"]+"\\hal\\hal"+str(usefulRecord.index(u))+".json"
        c="radon hal "+url+" --json --output-file \""+output_url+"\"\n"
        commands.append(c)
        output_url = "E:\\2020DataScience\\src\\method1\\PDI\\metrics\\" + v["case_id"] + "\\LLOC\\raw"+str(usefulRecord.index(u))+".json"
        c="radon raw "+url+" --json --output-file \""+output_url+"\"\n"
        commands.append(c)

print(commands)
with open('get_metrics.bat',mode='w') as f:
    f.writelines(commands)

