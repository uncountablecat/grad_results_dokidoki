import requests
import unicodecsv as csv
from bs4 import BeautifulSoup
import re

temp = []
results_holder = []
final_result = []

def scrape_data(major,page_num):
	global temp
	global results_holder

	feed_url = "http://thegradcafe.com/survey/index.php?q="+major+"&t=a&o=&p="+str(page_num)

	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

	# Get page source and parse it
	r = requests.get(feed_url, headers=headers)
	page_source = r.text
	soup = BeautifulSoup(page_source,"html.parser")

	# Look for the results in page source and write to results_holder
	for i in soup.find_all("tr",["row0","row1"]):
		for j in i:
			temp.append(j.get_text())
		if len(results_holder)==11:
			results_holder.append(temp[5:-1])
		else:
			results_holder.append(temp[:-1])
		temp = []

def isPhD(string):
	if any(x in string for x in ["phd","Phd","PhD"]):
		return "PhD"
	elif any(x in string for x in ["master","Master","masters","Masters"]):
		return "Master"
	else:
		return string
	# Don't forget the else branch
	# If you simply write else: pass, isPhD will return None

def resultAndGpa(string):
	if "GPA" in string:
		return string.split(" ")[0] + "," + re.search(r'[0-9]\.[0-9][0-9]',string).group()
	else:
		return string.split(" ")[0] + ",0"

def format_data():
	global results_holder
	global final_result
	
	# Get rid of the quotes
	results_holder = [map(lambda s:s.strip('\"'), x) for x in results_holder]
	results_holder = [map(isPhD, x) for x in results_holder]
	results_holder = [map(resultAndGpa, x) for x in results_holder]

	# print(results_holder)

def write_data():
	with open("results.csv","a") as csvfile:
		admission_results_writer = csv.writer(csvfile,delimiter=",",quoting=csv.QUOTE_NONE,quotechar='')
		for i in results_holder:
			admission_results_writer.writerow(i)

if __name__=='__main__':
	major_list = raw_input("Enter Majors, separated by comma:")
	for major in major_list.split(","):
		for page_num in range(1,3):
			scrape_data(major,str(page_num))
	format_data()
	write_data()
