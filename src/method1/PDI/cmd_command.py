import json
import os

f=open("s_pro_detail_dict.json",encoding="utf8")
res=f.read()
pro_dict=json.loads(res)


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
    if v["ans_is_py"]:
        url="F:\\2020Data\\200616\\src\\Preprocessing\\"+v["case_unzip_dir"]+".mooctest\\answer_modify.py"
    elif len(v["full_records"]) != 0:
        url = "F:\\2020Data\\200616\\src\\Preprocessing\\" + v["full_records"][0] + "main_modify.py"
    else:
        continue
    output_url="F:\\2020Data\\200616\\src\\method1\\PDI\\metrics\\"+v["case_id"]+"\\cc\\cc.json"
    c="radon cc "+url+" --show-complexity --json --output-file \""+output_url+"\"\n"
    commands.append(c)
    output_url="F:\\2020Data\\200616\\src\\method1\\PDI\\metrics\\"+v["case_id"]+"\\hal\\hal.json"
    c="radon hal "+url+" --json --output-file \""+output_url+"\"\n"
    commands.append(c)
    output_url = "F:\\2020Data\\200616\\src\\method1\\PDI\\metrics\\" + v["case_id"] + "\\LLOC\\raw.json"
    c="radon raw "+url+" --json --output-file \""+output_url+"\"\n"
    commands.append(c)

print(commands)
with open('get_metrics.bat',mode='w') as f:
    f.writelines(commands)

