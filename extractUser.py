#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from pdb import set_trace as bp
import io
prefix="people"
startNumber=2713
NumberofFiles=2928



count=0
file= io.open('myUserList.txt', 'w',encoding="utf-8")
for i in range(startNumber,NumberofFiles+1):
	print("Current Processing No."+str(i)+"/"+str(NumberofFiles))
	
#	bannedWords=['Hi '+MyUserName,'次',MyUserName,'/','一歌一遇','难得一面','世当珍惜'];
	try:
		tree = ET.parse('people'+str(i)+'.xml')
		root = tree.getroot()
		
		try:
			pattern2=root.find('.//node/node/node/node/node/node/node/node/node/node/node/node[2]/node/node/node[5]')
			text=pattern2.attrib["text"]
			#bp();
			#print("1"+text)
			if text!=u'次' and text!=u'难得一面' and text!=u'' :
				file.write(unicode(text)+'\n');
				count=count+1;
				continue
		except:
			pass

		try:
			pattern1=root.find('.//node/node/node/node/node/node/node/node/node/node/node/node[2]/node/node/node/node[5]/node[2]')
			text=pattern1.attrib["text"]
			#print("2"+text)
			if text!=u'次' and text!=u'难得一面' and text!=u'':
				file.write(unicode(text)+'\n');
				count=count+1;
				continue
		except:
			pass
		try:
			pattern3=root.find('.//node/node/node/node/node/node/node/node/node/node/node/node[2]/node/node/node[8]')
			text=pattern3.attrib["text"]
			#print("3"+text)
			#bp();
			if text!=u'次' and text!=u'难得一面' and text!=u'' :
				file.write(unicode(text)+'\n');
				count=count+1;
				continue
		except:
			pass
		print("No."+str(i)+" invalied data")
	except:
		print("No."+str(i)+" invalied data")
print("Finished, Valied Data:"+str(count))
