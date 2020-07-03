import json
import os
import shutil
import sys
from six.moves import urllib

# local_path = r'本地地址\2020DataScience\src\Preprocessing\'
# 手动复制绝对路径
local_path = ''


def download_and_extract(filepath, save_dir):
    for url, index in zip(filepath, range(len(filepath))):
        filename = url.split('/')[-1]
        save_path = os.path.join(save_dir, filename)
        urllib.request.urlretrieve(url, save_path)
        sys.stdout.write('\r>> Downloading %.1f%%' % (float(index + 1) / float(len(filepath)) * 100.0))
        sys.stdout.flush()
        print('\nSuccessfully downloaded')


# 目前用的数据还是s_record_dict.json
f = open("s_record_dict.json", encoding="utf8")
res = f.read()
data = json.loads(res)
data = list(dict.values(data))

# to = test oriented
to_dic = {}
# np = not python
np_dic = {}
# neither to nor np
valid_dic = {}
# abnormal = to or np
abn_dic = {}

for record in data:
    key = record["record_id"]
    if record["is_TO"]:
        to_dic[key] = record
        abn_dic[key] = record
    elif not record["is_py"]:
        np_dic[key] = record
        abn_dic[key] = record
    else:
        valid_dic[key] = record

# generate json
with open('abnormal_dict.json', 'w') as f:
    f.write(json.dumps(abn_dic, ensure_ascii=False, indent=4, separators=(',', ': ')))

with open('valid_dict.json', 'w') as f:
    f.write(json.dumps(valid_dic, ensure_ascii=False, indent=4, separators=(',', ': ')))


# get file
# abnormal sample
f = open("abnormal_dict.json", encoding="utf8")
res = f.read()
data = json.loads(res)
data = list(dict.values(data))

for rec in data:
    sd = os.path.abspath(local_path + 'abnormal_sample')
    file_path = os.path.abspath(local_path + 's_submit_code\\user_' + str(rec["user_id"]) + "\\" + str(rec["path_idx"]) + '_unzip')
    path_dir = os.listdir(file_path)
    to_path = sd + "\\" + 'user_' + str(rec["user_id"]) + "\\" + str(rec["path_idx"]) + '_unzip'

    if os.path.exists(file_path):
        shutil.copytree(file_path, to_path)

# valid sample
f = open("valid_dict.json", encoding="utf8")
res = f.read()
data = json.loads(res)
data = list(dict.values(data))

for rec in data:
    sd = os.path.abspath(local_path + 'valid_sample')
    file_path = os.path.abspath(local_path + 's_submit_code\\user_' + str(rec["user_id"]) + "\\" + str(rec["path_idx"]) + '_unzip')
    path_dir = os.listdir(file_path)
    to_path = sd + "\\" + 'user_' + str(rec["user_id"]) + "\\" + str(rec["path_idx"]) + '_unzip'

    if os.path.exists(file_path):
        shutil.copytree(file_path, to_path)