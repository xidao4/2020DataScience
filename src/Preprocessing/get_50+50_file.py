import json
import os
import shutil

# local_path = r'本地地址\2020DataScience\src\Preprocessing\'
# 手动复制绝对路径
local_path = ''

# abnormal sample
f = open("fifty_abnormal_dict.json", encoding="utf8")
res = f.read()
data = json.loads(res)
data = list(dict.values(data))

for rec in data:
    sd = os.path.abspath(local_path + 'fifty_abnormal_sample')
    file_path = os.path.abspath(local_path + 's_submit_code\\user_' + str(rec["user_id"]) + "\\" + str(rec["path_idx"]) + '_unzip')
    path_dir = os.listdir(file_path)
    to_path = sd + "\\" + 'user_' + str(rec["user_id"]) + "\\" + str(rec["path_idx"]) + '_unzip'

    if os.path.exists(file_path):
        shutil.copytree(file_path, to_path)

# valid sample
f = open("fifty_valid_dict.json", encoding="utf8")
res = f.read()
data = json.loads(res)
data = list(dict.values(data))

for rec in data:
    sd = os.path.abspath(local_path + 'fifty_valid_sample')
    file_path = os.path.abspath(local_path + 's_submit_code\\user_' + str(rec["user_id"]) + "\\" + str(rec["path_idx"]) + '_unzip')
    path_dir = os.listdir(file_path)
    to_path = sd + "\\" + 'user_' + str(rec["user_id"]) + "\\" + str(rec["path_idx"]) + '_unzip'

    if os.path.exists(file_path):
        shutil.copytree(file_path, to_path)