import ijson
import json
import os
f=open('packets')
g=open("answer","w")
parser=ijson.parse(f)
g.write("[")
d={}
for prefix,the_type,value in parser:
	# print(prefix, the_type, value)
	
	if (prefix , the_type ) == ("item._source.layers.ip.ip.proto" , "string"):
		d["proto"]=value
	elif (prefix , the_type ) == ("item._source.layers.ip.ip.src" , "string"):
		# print("fdafdafd")
		d["srcip"]=value
		x=value
		print(x)
	elif (prefix , the_type ) == ("item._source.layers.ip.ip.dst" , "string"):
		d["dstip"]=value
	
	elif (prefix , the_type ) == ("item._source.layers.tcp.tcp.len" , "string"):
		d["payloadLen"]=value
		g.write(json.dumps(d))
		g.write(",\n")


# remove the last added commma
g.seek(-2,os.SEEK_CUR)
g.truncate()

g.write("\n]")