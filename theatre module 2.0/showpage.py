#sample URL
#http://in.bookmyshow.com/buytickets/bridge-of-spies-chennai/movie-chen-ET00034536-MT/20151104

import urllib2
from bs4 import BeautifulSoup
import MySQLdb

db=MySQLdb.connect("localhost","","","theatre")
cursor=db.cursor()

f=open("page.html","w")
def showpage(edetails,place,placec,tdate):
	url="http://in.bookmyshow.com/buytickets/"+edetails["Event"]["EventUrlTitle"]+"-"+place.lower()+"/movie-"+placec+"-"+edetails["Event"]["EventCode"]+"-MT/"+str(tdate)
	print url
	page=urllib2.urlopen(url).read()
	soup=BeautifulSoup(page)
	for i in soup.find_all("a",class_="__name"):
			tpage=page
			print i
			f.write(str(tpage))
			tpage=tpage.split(str(i),1)
			print tpage[1]
			#tpage=tpage[1]
			tpage=tpage.split('''<div class="body">''',1)
			tpage=tpage[1]
			tpage=tpage.split("</div>",1)
			tpage=tpage[0]
			tb=BeautifulSoup(tpage)
			print tb.get_text(",")

	return
