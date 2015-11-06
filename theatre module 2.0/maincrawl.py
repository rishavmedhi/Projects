#http://in.bookmyshow.com/serv/getData.bms?cmd=SYNOPSISDATA&event_code=ET00035260&action=Synopsis

import datetime
import time
import MySQLdb
from bs4 import BeautifulSoup
import urllib2
from showpage import *

import pymongo
client = pymongo.MongoClient()
mdb=client['theatre']
qb=mdb['movies']

t_date=time.strftime("20%y%m%d")
db=MySQLdb.connect("localhost","","","theatre")
cursor=db.cursor()
up_time = datetime.datetime.now()
sql="SELECT `name`,`code` from `citynew`;"
cursor.execute(sql)
results=cursor.fetchall()

for row in results:
	r=str(row[0])
	r=r.replace(" ","-")
	r=r.replace("(","")
	r=r.replace(")","")
	c=str(row[1])
	print r
	url="http://in.bookmyshow.com/"+r+"/movies/nowshowing"
	page=urllib2.urlopen(url).read()
	soup=BeautifulSoup(page)
	mdiv=soup.find("div",class_="mv-row")
	for i in mdiv.find_all("div",class_="wow fadeIn movie-card-container"):
		#detail=i.find("img")
		detail=i.find("div",class_="__name")
		a=detail.find("a")
		movie_name=a.get('title')
		movie_code=a.get('href').rsplit("/",1)
		movie_code=str(movie_code[1]).replace(".jpg","")
		print movie_name,movie_code	
		url1="http://in.bookmyshow.com/serv/getData.bms?cmd=SYNOPSISDATA&event_code="+movie_code+"&action=Synopsis"
		data=urllib2.urlopen(url1).read()
		data="event_details="+data
		exec(str(data))	
		if qb.find({"Event.EventCode":str(movie_code)}).count()==0:
			qb.insert(event_details)
			showpage(event_details,r,c,t_date)
		else:
			showpage(event_details,r,c,t_date)
		break	