'''
	showpage(edetails,place,placec,tdate)
it's a function that extracts the theatre names and show timings of the theatres that are showing 
movie
	edetails:json of entire movie details
	place: place to be checked
	placec: code of place... as per website
	tdate: today's date in yyyymmdd
''' 

import urllib2
from bs4 import BeautifulSoup

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
	return theatre_list,time