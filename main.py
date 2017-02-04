import re
import requests
import unicodecsv as csv

from bs4 import BeautifulSoup
from itertools import chain
from datetime import datetime

temp = []
results = []
marker = datetime.strptime('1 Jan 2017', '%d %b %Y') # Set this time accordingly

def scrape_data(major,page_num):
	global temp
	global results

	feed_url = "http://thegradcafe.com/survey/index.php?q="+major+"&t=a&o=&p="+str(page_num)

	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

	# Get page source and parse it
	r = requests.get(feed_url, headers=headers)
	page_source = r.text
	soup = BeautifulSoup(page_source,"html.parser")

	# Look for the results in page source and write to results
	for i in soup.find_all("tr",["row0","row1"]):
		for j in i:
			temp.append(j.get_text())
		if len(results)==11:
			results.append(temp[5:-1])
		else:
			results.append(temp[:-1])
		temp = []

		
def isPhD(string):
	if any(x in string for x in ["phd","Phd","PhD"]):
		return "PhD"
	elif any(x in string for x in ["master","Master","masters","Masters"]):
		return "Master"
	else:
		return string
	# Don't forget the else branch
	# If you simply write else: pass, isPhD() will return None

	
def resultAndGpa(string):
	if any(x in string for x in ["Accepted","Rejected","Wait","Interview","Other"]):
		if "GPA" in string:
			return [string.split(" ")[0], re.search(r'[0-9]\.[0-9][0-9]',string).group()]
		else:
			return [string.split(" ")[0], 0]
	else:
		return string
	

def containAppliedSchool(string):
	'''
	You will have to modify this function
	according to what schools you have applied to
	'''
	if any(x in string for x in ["UNC","Washington"]):
		return True
	else:
		return False
	

def formatSchoolName(string):
	'''
	You will have to modify this function
	according to what schools you have applied to
	'''
	if any(x in string for x in ["UNC","Chapel","Chapel Hill"]):
		return "UNC"
	elif any(x in string for x in ["Washington Seattle","Washington"]):
		return "Washington"
	else:
		return string

	
def format_data():
	global results

	results = [record for record in results if len(record)>0]
	
	results = [record for record in results if containAppliedSchool(record[0])==True]
	results = [[formatSchoolName(record[0])] + record[1:] for record in results]
	results = [map(lambda s:s.strip('\"'), x) for x in results]
	results = [map(isPhD, x) for x in results]
	results = [map(resultAndGpa, x) for x in results]

	# Want to flatten things like [u'Rejected', u'3.94']
	for i in range(0,len(results)):
		results[i] = list(chain(results[i][:2],results[i][2],results[i][3:]))

		
def write_data(major):
	with open(major+"_results.csv","a") as csvfile:
		admission_results_writer = csv.writer(csvfile,delimiter=",")
		for i in results:
			if datetime.strptime(i[-1],'%d %b %Y') > marker:
				admission_results_writer.writerow(i)
			else:
				pass

if __name__=='__main__':
	for page_num in range(1,15): # You may need to modify this range
		print("Fetching data, page " + str(page_num))
		scrape_data("Statistics",str(page_num))

	print("Formatting data...")
	format_data()
	
	print("Writing data to csv...")
	write_data("Statistics")
