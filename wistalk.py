import sys
from bs4 import BeautifulSoup
import requests
import urllib.parse as urlparse
from urllib.parse import parse_qs
import datetime
import lxml


def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)



uname = sys.argv[1]
try:
	subwiki = sys.argv[2]
except Exception as e:
	subwiki = 'id'

if subwiki == 'en':
	url = "https://en.wikipedia.org/w/index.php?title=Special:Contributions/"+str(uname)+"&dir=prev&target=GeoWriter"
	baseurl = "https://en.wikipedia.org"
else:
	url = "https://id.wikipedia.org/w/index.php?title=Istimewa:Kontribusi_pengguna/"+str(uname)+"&dir=prev&limit=500"
	baseurl = "https://id.wikipedia.org"

stop = False
wikiarticle = set()
byte_add = 0
byte_rem = 0
stage = 0
topart = dict()

while not stop:

	stage += 500
	#print("Edit count : "+str(stage))

	parsed = urlparse.urlparse(url)
	try:
		x = parse_qs(parsed.query)['offset']
		dobj = datetime.datetime.strptime(x[0],'%Y%m%d%H%M%S')
		print(str(dobj) + "   " +str(stage) +" [+"+sizeof_fmt(byte_add)+"] ["+sizeof_fmt(byte_rem)+"]" )
	except Exception as e:
		None


	#print(url)
	actualPayload = bytearray()
	response = requests.get(url)
	actualPayload = response.text
	soup = BeautifulSoup(actualPayload,'lxml')

	titles = soup.find_all("a",{"class":"mw-contributions-title"})
	titles_time = soup.find_all("a",{"class":"mw-changeslist-date"})
	bytescontrib = soup.find_all("span",{"class":"mw-diff-bytes"})
	next_url = soup.find("a",{"class":"mw-prevlink"})
	theList = soup.findAll("li",{"data-mw-revid":True})


	theList.reverse()
	for i in theList:
		c_title = i.find("a",{"class":"mw-contributions-title"})
		c_time = i.find("a",{"class":"mw-changeslist-date"})
		c_ctr = i.find("span",{"class":"mw-diff-bytes"})
		c_diff = i.find("a",{"class":"mw-changeslist-diff"})


		try:
			a = c_ctr.text.replace("−","-")
			a = int(a)
			if c_title.text not in topart:
				topart[c_title.text] = a
			else:
				topart[c_title.text] += a
			print(c_time.text +" : "+c_title.text + " (" + c_ctr.text +" / "+str(topart[c_title.text]) +")")
			
		except Exception as e:
			
			try:
				print(c_time.text +" : "+c_title.text)
			except Exception as d:
				print(c_title.text)
		try:
			print(baseurl+c_diff.attrs["href"])
		except Exception as e:
			try:
				print(baseurl+c_time.attrs["href"]+"  (B)")
			except Exception as e:
				continue
		print()



	

	
	for i in bytescontrib:
		#print(i.text)
		a = i.text.replace("−","-")
		contrib = int(a)
		if contrib >= 0:
			byte_add += contrib
		else:
			byte_rem += contrib


	try :
		next_url = next_url.attrs["href"]
		url = baseurl + next_url
	except Exception as e:
		stop = True


'''
for i in wikiarticle:
	print(i)
'''


for i in sorted(topart,key=topart.get,reverse=False):
	print(str(i) +" : "+ str(topart[i])) 
print()

print("Addition "+sizeof_fmt(byte_add))
print("Deletion "+sizeof_fmt(byte_rem))


