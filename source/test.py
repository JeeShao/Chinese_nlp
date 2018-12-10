import jieba
import jieba.posseg as pseg

# seg_list=[]
line='"一带一路"倡议提出以来,我国已在高校非英语语种专业招生、学科设置上做出调整,在英语语种人才培养方面提出了复合型人才的培养模式。'
# seg_list=jieba.cut(line,cut_all=True)
# print("Full Mode:","/ ".join(seg_list))#全模式
 
# seg_list=jieba.cut(line,cut_all=False)
# print("Default Mode:","/ ".join(seg_list))#精确模式
 
# seg_list=jieba.cut(line)#默认是精确模式
# print(", ".join(seg_list))
 
# seg_list=jieba.cut_for_search(line)#搜索引擎模式
# print(", ".join(seg_list))


for w in pseg.cut(line):
	print (w.word,w.flag)

