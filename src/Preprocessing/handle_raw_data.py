import json
import urllib.request,urllib.parse
import os
import zipfile

#把src_zip解压缩，存到dest_dir中
def unzip(src_zip,dest_dir):
    if zipfile.is_zipfile(src_zip):
        zip_file=zipfile.ZipFile(src_zip,'r')
        for file in zip_file.namelist():
            zip_file.extract(file,dest_dir)
    else:
        print('第一个参数的路径'+src_zip+'不是压缩包，解压缩失败')

def remove_zip(zip_path):
    if os.path.exists(zip_path):
        os.remove(zip_path)
        print('路径'+zip_path+'解压后，完成删除操作')
    else:
        print('路径'+zip_path+'不存在，为什么要删除？')

#Testcases Oriented Programming
def TO(path):
    fp=open(path,encoding="utf8")
    isTO=False
    suspected=0
    former_line=""
    line_num = 0 #suspected/line_num的比例高于阈值，判定为TO
    print_num=0 #print出现超过20次，判定为TO。print行数/总行数比例过高。

    for l in fp.readlines():
        l=l.lstrip()#用于截掉字符串左边的空格或指定字符
        if not(l.startswith("#")):#非注释
            line_num+=1
        else:#该行是注释，不算入行数，直接跳过
            former_line=l
            continue

        #看这行代码是否有TO的嫌疑
        if l.startswith("print"):
            print_num+=1

        if l.startswith("print") and former_line.startswith("if"):
            suspected += 1
        elif l.startswith("print") and former_line.startswith("elif"):
            suspected+=1
        elif l.startswith("print") and former_line.startswith("else"):
            suspected+=1

        former_line=l

    if print_num>20: isTO=True #print出现超过20次，判定为TO。
    elif line_num>0 and suspected/line_num>=0.3: isTO=True #suspected/line_num的比例高于阈值，判定为TO
    elif line_num>0 and print_num/line_num>=0.9: isTO=True #print行数/总行数比例过高。

    return isTO

def get_inner(dir):
    inner=[]
    for root,dirs,files in os.walk(dir):
        for file in files:
            inner.append(os.path.join(root,file))
    return inner

f=open('sample.json',encoding='utf-8')
res=f.read()
data=json.loads(res)#加载json数据
#报错 KeyError: 0    解决办法:把字典类型的data的值变成列表,列表里的元素是字典
data=list(dict.values(data))

handled_dict={}
for user in data:
    cases=user["cases"]
    pre="all_submit_code\\user_"+str(user["user_id"])
    if not os.path.exists(pre):
        os.mkdir(pre)
    for case in cases:
        print(case["case_id"],case["case_type"])
        max_score=0
        case["case_TO"]=False
        for record in case["upload_records"]:
            filename=urllib.parse.unquote(os.path.basename(record["code_url"]))#url最后一个/后的内容，解码为中文
            print(filename)

            zip_url=pre+"\\"+filename
            try:
                urllib.request.urlretrieve(record["code_url"],zip_url)
                #第一个参数：外部url
                #第二个参数：指定了保存到本地的路径（如果未指定该参数，urllib会生成一个临时文件来保存数据）
            except Exception as e:
                print("下载提交代码失败",e)

            unzip_dir = pre + "\\" + filename + "_unzip\\"
            if not os.path.exists(unzip_dir):
                os.mkdir(unzip_dir)
            try:
                unzip(zip_url,unzip_dir)#外层解压
                remove_zip(zip_url)#解压后删除压缩包

                inner_zip=get_inner(unzip_dir)[0]#获取内层的压缩包
                unzip(inner_zip,unzip_dir)#内层解压缩，把inner_zip解压缩，存到unzip_dir中
                remove_zip(inner_zip)
            except Exception as e:
                print(e)

            code_url=unzip_dir+"main.py"
            isTO=TO(code_url)#打开main.py然后判断TO
            print(isTO)
            if isTO:
                record["TO"]=True
                record["score"]=0
                case["final_TO"]=True
            else:
                record["TO"]=False
            max_score=max(max_score,record["score"])
        case["case_score"]=max_score
    handled_dict[user["user_id"]]=user
json_handled=json.dumps(handled_dict,ensure_ascii=False, indent=4)
with open('handled_data.json','w') as f:
    f.write(json_handled)
# cases=data[0]['cases']#取出json中第一个学生的cases数据
# for case in cases:
#     print(case["case_id"],case["case_type"]);
#     #获取文件名（url里对中文会urlencode），解码
#     filename=urllib.parse.unquote(os.path.basename(case["case_zip"]))#url里最后一个/后的内容作为文件名
#     print(filename)
#     #下载题目包到本地
#     url=urllib.parse.quote(case["case_zip"],safe=";/?:@&=+$,")#编码url里的中文
#     urllib.request.urlretrieve(url,filename)