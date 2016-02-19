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

db=MySQLdb.connect("localhost","root","1","theatre")
cursor=db.cursor()

count=0
f=open("error","a")
t_date=time.strftime("20%y%m%d")
up_time = datetime.datetime.now()

def setProxy():
	proxy_handler = urllib2.ProxyHandler({})
	opener = urllib2.build_opener(proxy_handler)
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	urllib2.install_opener(opener)

def chngcity(name):
	sql1="SELECT `place` from `ncrtheatre` where `theatrename` REGEXP '%s';"%(str(name))
	res=cursor.execute(sql1)
	if not res:
		return "ncr"
	else:
		r=str(cursor.fetchone())
		r=r.replace("(","")
		r=r.replace(")","")
		r=r.split("'",1)
		r=r[1]
		r=r.split("'",1)
		r=r[0]
		return str(r)

def sepcraw(r,c):
	global count
	setProxy()
	print r
	url="http://in.bookmyshow.com/"+r+"/movies/nowshowing"
	try:
		page=urllib2.urlopen(url).read()
		soup=BeautifulSoup(page)
		mdiv=soup.find("div",class_="mv-row")
		for i in mdiv.find_all("div",class_="wow fadeIn movie-card-container"):
			#detail=i.find("img")
			try:
				th_list=[]
				sh_times=[]
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
					th_list,sh_times=showpage(event_details,r,c,t_date)
				else:
					th_list,sh_times=showpage(event_details,r,c,t_date)
				
				genre=str(event_details["Event"]["EventGenre"]).replace("|",",")		
				synopsis=MySQLdb.escape_string(str(event_details["Event"]["EventSynopsis"]))
				
				#http://in.bmscdn.com/Events/Large/ET00027655.jpg       sample image URL
				image="http://in.bmscdn.com/Events/Large/"+str(event_details["Event"]["EventCode"])+".jpg"   
				
				if event_details["Event"]["EventDuration"]==0:
					event_details["Event"]["EventDuration"]=""
			except Exception as e:
				print str(e)
				time.sleep(30)
				f.write("MOVIE :: "+str(movie_code)+str(r)+str(e)+"\n")
				pass
			
			for i in range(0,len(th_list)):
				try:
					th=str(th_list[i])
					j=MySQLdb.escape_string(str(sh_times[i]))
					sql1="SELECT * from `showtimes2` where `theatrename`='%s' and `moviecode`='%s';"%(str(th),str(movie_code))
					res=cursor.execute(sql1)
					if not res:
						if(r=="ncr"):
							r=chngcity(th_name)
						sql2='''INSERT INTO `showtimes2`(`theatrename`,`city`,`citycode`,`moviename`,`moviecode`,`shwtimes`,`updatetime`,`img_link`,`releasedate`,`duration`,`director`,`language`,`genre`,`cast`,`rating`,`synopsis`) VALUES("%s","%s","%s","%s","%s","%s",'%d','%s','%s','%s','%s','%s','%s','%s','%s','%s');'''%(str(th),str(r),str(c),str(movie_name),str(movie_code),str(j),int(t_date),str(image),str(event_details["Event"]["ReleaseDate"]),str(event_details["Event"]["EventDuration"]),str(event_details["Event"]["EventDirector"]),str(event_details["Event"]["EventLanguage"]),str(genre),str(event_details["Event"]["EventStarring"]),str(event_details["Event"]["EventCensor"]),str(synopsis))
						cursor.execute(sql2)
						db.commit()
						count=count+1
						print "within res"
						print str(count)+" data entered\n"
					else:
						sql3="UPDATE `showtimes2` SET `shwtimes`='%s', `updatetime`='%d' where `theatrename`='%s' and `moviecode`='%s';"%(str(j),int(t_date),str(th),str(movie_code))
						cursor.execute(sql3)
						db.commit()
						count=count+1
						print "within else"
						print str(count)+" data retained/updated\n"
					if count%20==0:
						time.sleep(15)

						
				except Exception as e:
					print str(e)
					time.sleep(30)
					f.write("DATABASE :: "+str(movie_code)+str(r)+str(e)+"\n")
					pass

	except Exception as e:
		print str(e)
		time.sleep(30)
		f.write("CITY :: "+str(movie_code)+" "+str(r)+" "+str(e)+"\n")
		pass

	sql4="DELETE from `showtimes2` where `updatetime`<'%d';"%(int(t_date))
	cursor.execute(sql4)
	db.commit()
	db.close()