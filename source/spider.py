#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import re
import csv
import time
import sys
import io
import requests
from bs4 import BeautifulSoup
from selenium import webdriver  #导入Selenium的webdriver
from selenium.webdriver.common.keys import Keys  #导入Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def mkdir(path):
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path) 
        print (path+' 创建成功')
        return True
    else:
        print (path+' 目录已存在')
        return False

def delete_file_folder(src):
    if os.path.isfile(src):
        try:
            os.remove(src)
        except:
            pass
    elif os.path.isdir(src):
        for item in os.listdir(src):
            itemsrc=os.path.join(src,item)
            delete_file_folder(itemsrc) 
        try:
            os.rmdir(src)
        except:
            pass

#保存摘要 name.txt
def save_abstract(file,str):
	try:
		with open(file,'w') as f:
			f.write(str)
	except Exception as err:
		print(file,err)
		pass

'''
根据期刊年获取该年各期url 
@return:url list
'''
def get_terms_url_by_year(driver,year_elem):
	urls=[]
	year_elem.click()
	# time.sleep(0.5)
	WebDriverWait(driver, 20).until(lambda s: s.execute_script("return jQuery.active == 0"))#根据jquery是否执行完毕来判定ajax加载完毕 （也可用selenium的隐式等待）
	terms = driver.find_elements_by_xpath("//div[@class='pakage r-bian']")
	for term in terms:
		text = term.find_element_by_tag_name("div").get_attribute("title")#2018年第05期
		url = term.find_element_by_tag_name("a").get_attribute("href")#2018年第05期的url
		print(url)
		urls.append(url)
	return urls

def get_abstract_by_url(driver,url,year_dir):
	all_div,titles=[],[]
	paper_url,title_name='',''
	dicts={}

	driver.get(url)  #请求网页地址
	time.sleep(0.5)
	# try:
	# 	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "p02-l-tit")))#等待进入期刊
	# finally:
	# 	driver.quit()

	global writer
	
				        
	soup = BeautifulSoup(driver.page_source, 'lxml')
	all_div = soup.find('div',id='divCJFDCatalog').find_all('div',class_='l-box')#获取栏目
	for div in all_div:
		if not div.find('div').string:
			continue
		column = div.find('div').string.strip() #栏目名
		if column:
			tab_lefts = div.find_all('div',class_='tab-left')
			titles=[i.find('a') for i in tab_lefts]#<a href>文章名称</a>
			for title in titles:
				content=[]
				abstract=''
				title_name=(title.string).strip()
				paper_url=title['href']

				print(paper_url)
				driver.get(paper_url)
				time.sleep(0.5)
				# try:
				# 	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "down_1")))#等待进入文章
				# finally:
				# 	driver.quit()
				soup = BeautifulSoup(driver.page_source, 'lxml')
				try:#部分老文章文没有摘要
					abstract = soup.find('div', style="text-align:left;word-break:break-all").get_text()
					content = abstract.split('：',1)[1]
				except Exception:
					content.append('正')
				if content[0]!='正' and zh_pattern.search(title_name):
					print(title_name)
					writer.writerow([title_name,paper_url])#存入paper_urls.csv
					file = os.path.join(year_dir,title_name.replace('/','').replace('?','').replace(':','')+'.txt')#去除文章名中的'/'  去除标点=> ''.join(e for e in key if e.isalnum())
					print(file)
					save_abstract(file,content)

def main():
	URL = {"a外语教学与研究":"http://yuanjian.cnki.net/CJFD/Detail/Index/WJYY",
	       "c上海外国语大学学报":"http://yuanjian.cnki.net/CJFD/Detail/Index/WYXY"}
	PATH = '../摘要文件'
	mkdir(PATH)
	driver = webdriver.Chrome()  #指定使用的浏览器，初始化webdriver
	driver.implicitly_wait(10) # seconds
	start_year=2018 #最近的年
	end_year = 2014
	start=int(2018-start_year+1)
	end=int(2018-end_year+2)
	for journal_name,journal_url in URL.items():
		print(journal_name)
		journal_dir = os.path.join(PATH,journal_name)
		mkdir(journal_dir)
		BASE_URL = journal_url#上海外国语大学学报
		
		for n in range(start,end):#遍历每一年期刊
			driver.get(BASE_URL)  #请求网页 	
			soup = BeautifulSoup(driver.page_source, 'lxml')
			journal_years = soup.find('div',class_="part03").find_all('span')[1:11]#获取近10年
			year = driver.find_element_by_xpath("//div[@class='part03']/span[%d]"%(n+1))
			print(year.text)
			year_dir=os.path.join(journal_dir,year.text.split(' ')[0])#分割“2018 年”=>2018
			mkdir(year_dir) #创建期刊年文件夹
			for i in os.listdir(year_dir):#清空原本文章文件
				delete_file_folder(os.path.join(year_dir,i))
			urls = get_terms_url_by_year(driver,year)#urls=>每个期刊的入口url
			for url in urls:#遍历每一期
				print(url)
				get_abstract_by_url(driver,url,year_dir)#获取每期文章摘要并写入文件
	f.close()
	driver.close()

if __name__ == '__main__':
	zh_pattern = re.compile(u'[\u4e00-\u9fa5]+') #判断中文
	csv_header=['题目','URL']
	f = open('../摘要文件/paper_urls.csv','w',newline='')
	writer = csv.writer(f)
	writer.writerow([csv_header])
	main()