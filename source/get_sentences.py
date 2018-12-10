import os
import re
import common
import jieba.posseg as pseg

'''
对摘要进行分句，返回分句list
'''
def splitSentence(file):
	data=[]
	f=open(file,'r')
	lines=f.readlines()
	for line in lines:
		sen_list=[]
		sentences = re.split('(。|！|\!|？|\?)',line)
		for i in range(int(len(sentences)/2)):
		    sent = sentences[2*i] + sentences[2*i+1]
		    sen_list.append(sent)
		data.extend(sen_list)
	f.close()
	return data	

'''
分句
'''
def get_sentences(dir):
	parent_dir = os.path.abspath(os.path.dirname(os.getcwd()))#C:\Users\jee_s\Desktop\助研\中文语料处理
	orgDir = os.path.join(parent_dir,"摘要文件")
	toDir  = os.path.join(parent_dir,dir)
	common.mkdir(toDir)
	all_dirs, all_files, all_names = common.getdir(orgDir)
	for i in all_files[1:]: #所有摘要文件
		print(i)
		filename = os.path.basename(i)
		# print(os.path.splitext(i))
		sents = splitSentence(i)
		common.save_file(sents,os.path.join(toDir,filename)) 

if __name__ == '__main__':
	get_sentences('分句语料库')