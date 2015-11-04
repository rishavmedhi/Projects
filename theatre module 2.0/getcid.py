import MySQLdb
import urllib2

def setProxy():
	proxy_handler = urllib2.ProxyHandler({'http':'172.16.0.16:8080'})
	opener = urllib2.build_opener(proxy_handler)
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	urllib2.install_opener(opener)
#setProxy()

db=MySQLdb.connect("localhost","","","theatre")
cursor=db.cursor()

url="http://in.bookmyshow.com/serv/getData/?cmd=GETREGIONS"
page=urllib2.urlopen(url).read()
page=page.replace("var","")
page=page.strip()
exec(str(page))
del regionlst["Spain"]
del regionlst["UAE"]
del regionlst["Singapore"]
del regionlst["United Kingdom"]
del regionlst["Vietnam"]
st_keys=regionlst.keys()
for i in st_keys:
	for j in regionlst[i]:
			state=str(i)
			city=str(j["name"])
			code=str(j["code"])
			sql="INSERT INTO `citynew`(`name`,`code`,`state`) VALUES ('%s','%s','%s');"%(city,code,state)
			cursor.execute(sql)
			db.commit()
db.close()