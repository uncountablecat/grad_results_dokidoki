import requests
import unicodecsv as csv
from bs4 import BeautifulSoup

def main(major,page_num):
	feed_url = "http://thegradcafe.com/survey/index.php?q="+major+"&t=a&o=&p="+str(page_num)

	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

	results_holder = [0]*5

	# Get page source and parse it
	r = requests.get(feed_url, headers=headers)
	page_source = r.text
	soup = BeautifulSoup(page_source,"html.parser")

	# Look for the results in page source and write to csv
	with open("results.csv","a") as csvfile:
		admission_results_writer = csv.writer(csvfile,delimiter=",")
		for i in soup.find_all("tr",["row0","row1"]):
			for j in i:
				results_holder.append(j.get_text())
			if len(results_holder)==11: # some results have [0,0,0,0,0] in front of it. Reason unknown, yet
				admission_results_writer.writerow(results_holder[5:-1])
			else:
				admission_results_writer.writerow(results_holder[:-1])
			results_holder = []

if __name__=='__main__':
	major_list = raw_input("Enter Majors, separated by comma:")
	for major in major_list.split(","):
		for page_num in range(1,7):
			main(major,str(page_num))
