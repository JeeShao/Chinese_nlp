import jieba.posseg as pseg
import common
import os

def pos_tag(file):
	data,stens=[],[]
	f=open(file,'r')
	lines=f.readlines()
	for line in lines:
		# if len(line)>1:
		line = line.strip('\n') #去除末尾换行符
		stens=[]
		for word,pos in pseg.cut(line):
			stens.append(word+'_'+pos)
		# stens=[word+'_'+pos for word,pos in pseg.cut(line)]
		data.append(' '.join(stens))
	f.close()
	return data

parent_dir = os.path.abspath(os.path.dirname(os.getcwd()))#C:\Users\jee_s\Desktop\助研\中文语料处理
src_dir = os.path.join(parent_dir,"分句语料库")
dst_dir = os.path.join(parent_dir,"附码语料库")
common.mkdir(dst_dir)
_,files,_ = common.getdir(src_dir)
for file in files:
	print(file)
	filename = os.path.basename(file)
	data = pos_tag(file)
	common.save_file(data,os.path.join(dst_dir,filename))