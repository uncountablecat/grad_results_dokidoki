import requests
import unicodecsv as csv
#import csv
from bs4 import BeautifulSoup

# feed_url = "http://thegradcafe.com/survey/index.php"
feed_url = "http://thegradcafe.com/survey/index.php?t=m&o=&p=3"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

results_holder = [0]*5

# Get page source and parse it
r = requests.get(feed_url, headers=headers)
page_source = r.text
soup = BeautifulSoup(page_source,"html.parser")

# Look for the results in page source
with open("results.csv","wb") as csvfile:
	admission_results_writer = csv.writer(csvfile,delimiter="\t")
	for i in soup.find_all("tr",["row0","row1"]):
		for j in i:
			results_holder.append(j.get_text())
		admission_results_writer.writerow(results_holder)
		results_holder = []
