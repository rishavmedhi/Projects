#http://in.bookmyshow.com/buytickets/bridge-of-spies-chennai/movie-chen-ET00034536-MT/20151104
import urllib2
from bs4 import BeautifulSoup
import MySQLdb

db=MySQLdb.connect("localhost","root","1","theatre")
cursor=db.cursor()

def showpage(edetails,place,placec,tdate):
	url="http://in.bookmyshow.com/buytickets/"+edetails["Event"]["EventUrlTitle"]+"-"+place.lower()+"/movie-"+placec+"-"+edetails["Event"]["EventCode"]+"-MT/"+str(tdate)
	print url
	page=urllib2.urlopen(url).read()
	soup=BeautifulSoup(page)
	part=soup.find("section",class_="phpShowtimes showtimes")
	theatre_wlist=part.find_all("a",class_="__name")
	time_body=part.find_all("div",class_="body")	
	theatre_list=[]
	tlist=[]
	time=[]
	ctr=0
	
	for i in theatre_wlist:
		i=str(i)
		i=i.split("<strong>",1)
		i=i[1]
		i=i.split("</strong>",1)
		i=i[0]
		i=i.replace(":","")
		theatre_list.append(i)

	for j in time_body:
		a=j.find_all("a")
		tlist=[]
		for k in a:
			tlist.append(str(k.get_text()))
		time.append(tlist)
	print len(theatre_list),len(time)
	return theatre_list,time

#showpage()
#showpage("bridge-of-spies","chennai","chen","ET00034536","20151104")