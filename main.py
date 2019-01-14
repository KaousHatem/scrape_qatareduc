import requests
from bs4 import BeautifulSoup
from pandas import ExcelWriter
import pandas as pd

BASE_URL = "http://qatareducationaldirectory.qa/"
URL_CATEGORY = BASE_URL+"PageResult.aspx?category=7"

HEADERS = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
	} 

dict_detail = {'Address':'None',
			   'Tel':'None',
			   'Fax':'None',
			   'E-mail':'None', 
			   'Website':'None',
			   'Location':'None',
			   'Curriculum':'None',
			   }
def log_i(log,code):
	print('[+]-----code:',code,' __ ',log)

def log_e(log,code):
	print('[-]-----code:',code,' __ ',log)


#this function return a list of links that refer to a school
def get_list_educ():
	response_link = requests.get(URL_CATEGORY, headers=HEADERS)
	soup = BeautifulSoup(response_link.text,'lxml')
	divs = soup.findAll('div',class_="listing-item")
	return [BASE_URL+div.find('h6').find('a').get('href') for div in divs]

def get_educ_detail(url_educ):
	print(url_educ)
	response_link = requests.get(url_educ, headers=HEADERS)
	soup = BeautifulSoup(response_link.text,'lxml')
	div = soup.find('div',class_='sidebar')
	if div == None:
		return {}
	uls = div.findAll('ul')
	for ul in uls[:-3]:
		tmp = dict_detail
		info = ul.find('li',class_='info').text[1:]
		detail = ul.find('li',class_='details').text
		if info not in tmp.keys():
			continue
		tmp[info]=detail
	tmp['Name']=soup.findAll('h4')[0].text

	return tmp

	
	


if __name__ == "__main__":
	list_educ = get_list_educ()
	all_info = [list(get_educ_detail(educ).values()) for educ in list_educ]
	print(all_info)
	columns = dict_detail.keys()
	df = pd.DataFrame(all_info, columns = columns)
	print(df)
	writer = ExcelWriter('Sports Academics In Qatar.xlsx')
	df.to_excel(writer,'Sheet1',index=False)
	writer.save()



