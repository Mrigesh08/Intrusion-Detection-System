# convert2.py
# used to convert JSON format to python array format

import ijson
import json
import os
from random import randint

writingInterval = 10 # write 1 random record to 'dstfilename' after 'writingInterval' records have been encountered
def convertIPtoInt(ipaddr):
	x=ipaddr.split(".")
	y=1
	s=0
	for i in range(3,-1,-1):
		s=s+(int(x[i]))*y
		y=y*255
	return s

# print(convertIPtoInt("0.0.0.1"))
# print(convertIPtoInt("0.0.1.0"))
# print(convertIPtoInt("0.1.0.0"))
# print(convertIPtoInt("1.0.0.0"))

def writeToFile(ls,f):
	x=randint(0,writingInterval-1)
	f.write(json.dumps(ls[x]))
	f.write(",\n")

def convert(srcfilename,dstfilename):	
	f=open(dstfilename,"w");
	f.write("arr=[\n");

	g = open(srcfilename)
	parser = ijson.parse(g)
	bigls=[]
	ls=[]
	i=0
	for prefix , event, value in parser:
		if (prefix , event) == ("item.srcip" , "string"):
			ls.append(convertIPtoInt(value))
		elif (prefix , event) == ("item.dstip" , "string"):
			ls.append(convertIPtoInt(value))
		elif (prefix , event) == ("item.payloadLen" , "string"):
			ls.append(int(value))
		elif (prefix , event) == ("item.proto" , "string"):
			ls.append(int(value))
			bigls.append(ls)
			ls=[]
			i=i+1
			if i==writingInterval:
				writeToFile(bigls,f)
				i=0
				bigls=[]

	f.seek(-2,os.SEEK_CUR)
	f.truncate()
	f.write("\n]")


srcfilename = "./answer"
dstfilename = "./pythonarr3.py"

convert(srcfilename,dstfilename)
