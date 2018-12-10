import os

def mkdir(path):
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
    # 判断路径是否存在
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path) 
        print (path+' 创建成功')
        return True
    else:
        print (path+' 目录已存在')
        return False

#返回所有目录名、文件路径、文件名
def getdir(path):
    all_file=[]
    all_name=[]
    all_dirs = []
    for root,dirs,files in os.walk(path):
        all_dirs.extend(dirs)
        for file in files:
            file=file.encode('utf-8').decode('utf-8')
            all_file.append(root+'\\'+file)
            all_name.append(file)
    return all_dirs,all_file,all_name

'''
保存分句文件
'''
def save_file(pre_data,path):
    f=open(path,'w')
    for row in pre_data:
        f.write(row+'\n')
    f.close()