#program to identify patterns in a given text
import time
import re
import pymongo
from bs4 import BeautifulSoup
client=pymongo.MongoClient()
mdb=client['text_mining']
db=mdb['minister']

objects=[]
#pronoun list
pronoun=["he","she","she","it"]

def fileopen(filename):
	f=open("file.txt","r")
	data=f.read()

#segmenting the document into segments
def text_miner(data):
	global objects
	print type(objects)
	if "(" in data and ")" in data:
		part1=data.split("(")
		part2=data.split(")")
		part1=part1[0]
		part2=part2[1]
		data=part1+part2
	#counting the no. of words
	tokens=data.split(" ")
	count=len(tokens)

	data=data.split(".")

	prev=False
	found={}
	prob={}
	found_list=[]
	last_obj=""
	prob["count"]=count 
	for i in data:
		i=i.strip()
		sentence=i
		m=re.findall(r'\swas the\s|\swas\s|\swas an\s|\swas a\s|\sis the\s|\sis an\s|\sis a\s|\sis\s',i)
		if len(m)!=0:
			for k in m:
				i=sentence
				found_list=found.keys()
				if str(k) in found_list:
					found[str(k)]+=1
				else:
					found[str(k)]=1
				print k
				i=i.split(k)
				obj=i[0].strip()
				desc=i[1].strip()
				for pp in pronoun:
					if pp in obj.lower() and prev==True:
						obj=re.sub(r'\.*\s*she\s|^she\s*|\.*\s+she\s+|\sshe|^he\s*|\.*\s+he\s+|\she'," "+last_obj+" ",obj.lower())
						print "converted"
						prev=True
					else:
						last_obj=obj
						if last_obj in pronoun:
							prev=False
						else:
							prev=True
				print "Object :"+obj
				print "Description :"+desc
				objects.append(obj)
				objects=list(set(objects))
	if len(found.keys())==0:
		print "NO DESCRIPTORS FOUND"
	for i in found.keys():
		prob[str(i)]=float(found[str(i)])/float(count)
	print prob


print "Enter the input method for data:\n1.From file\n2.From mongo database"
opt=input()
if(opt==1):
	filename=raw_input("Enter the filename : ")
	data=open(filename).read()
	text_miner(data)
elif (opt==2):
	print "accessing the database :"
	for i in db.find():
		data=i["Description"]
		soup=BeautifulSoup(data)
		text=soup.get_text()
		text_miner(text)
		#time.sleep(3)
print objects