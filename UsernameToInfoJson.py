#!/usr/bin/env python
#coding=utf-8

#using the api:https://github.com/Binaryify/NeteaseCloudMusicApi need login first
import datetime
import time
import requests
import json
import csv
from pdb import set_trace as bp
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
# def common_elements(list1, list2):
#     return [element for element in list1 if element in list2]
inFileName="myUserList.txt";
data={}
errorUser={}
#login:
phonenumber="***********"
password="********"
s = requests.session()
login=s.get("http://localhost:3000/login/cellphone?phone="+phonenumber+"&password="+password).json();
myLiked=s.get("http://localhost:3000/likelist?uid="+str(login["account"]["id"])).json() 
myLikedSongs=myLiked["ids"]
#------------------
def findCommonLikedSongs(matchUserID,myLikedSongs,s):


	UserPlayList=s.get("http://localhost:3000/user/playlist?uid="+str(matchUserID)).json()
	UserPlayListPool=[]
	for selectList in UserPlayList["playlist"]:
		if str(selectList["creator"]["userId"])==str(matchUserID) and selectList["playCount"]>=5:#选择自创的并且播放次数大于5次的歌单
			UserPlayListPool.append(selectList["id"])
	UserMusicPool={}
	for ids in UserPlayListPool:
		Songs=s.get("http://localhost:3000/playlist/detail?id="+str(ids)).json()
		for item in Songs["playlist"]["tracks"]:
			UserMusicPool[item["id"]]=item["name"]


	CommonLikedSongs=[]
	for myIDs in myLikedSongs:
		if myIDs in UserMusicPool:
			CommonLikedSongs.append(UserMusicPool[myIDs])

	return CommonLikedSongs


#------------------





countIteration=0;
with open('person.csv', 'w') as csvFile:
	writer=csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	writer.writerow(["用户名","ID","主页地址","生日","性别","等级","听歌数目","省份ID","城市ID","个性签名","社交网络","相同歌曲数目","共同歌曲列表"])
	with open(inFileName) as fp:
		for line in fp:
			countIteration+=1
			print("Processing No."+str(countIteration));
			username=unicode(line.strip("\n"))
	#read file start for loop
			userid=0;
			homePageUrl=""
			birthday=""
			gender=""
			level=0
			listenSongs=0
			provinceId=0
			cityId=0
			signature=""
			socialNet=[];


			try:
				#1.get user id

				user=s.get("http://localhost:3000/search?type=1002&keywords="+username).json()
				for userprofile in user['result']['userprofiles']:
					#bp()
					if username==userprofile['nickname']:
						userid=userprofile['userId']
						break
				if userid==0:
					print(username+"id not found!");
					errorUser[username]={"reason":"id not found"}
					continue
					#enter next user
				#2.get user info
				info=s.get("http://localhost:3000/user/detail?uid="+str(userid)).json()
				homePageUrl = 'https://music.163.com/#/user/home?id='+str(userid)
				#bp()
				if info["profile"]["birthday"] >0:
					birthday=datetime.datetime.utcfromtimestamp(info["profile"]["birthday"]/1000).strftime("%Y/%m/%d")
				level=info["level"]
				listenSongs=info["listenSongs"]
				provinceId=info["profile"]["province"]
				cityId=info["profile"]["city"]
				signature=info["profile"]["signature"]
				for binding in info["bindings"]:
					if binding["url"]:
						socialNet.append(binding["url"])
				if info["profile"]["gender"]==1:
					gender="男"
				elif info["profile"]["gender"]==2:
					gender="女"

				CommonLikedSongs=findCommonLikedSongs(userid,myLikedSongs,s)
				NumberofCommonSongs=len(CommonLikedSongs)

				data[username]={
					"username":username,
					"userId":userid,
					"homePageUrl":homePageUrl,
					"birthday": birthday,
					"gender":gender,
					"level":level,
					"listenSongs":listenSongs,
					"provinceId":provinceId,
					"cityId":cityId,
					"signature":signature,
					"socialNet":socialNet,
					"numberofCommonSongs":NumberofCommonSongs,
					"commonLikedSongs":CommonLikedSongs
					}

				
				LikedSongsList=""
				for songs in CommonLikedSongs:
					LikedSongsList=LikedSongsList+" | "+songs.encode('utf-8')
				writer.writerow([username,str(userid),homePageUrl,birthday,gender,str(level),\
					str(listenSongs),str(provinceId),str(cityId),signature.encode('utf-8')\
					,socialNet,str(NumberofCommonSongs),LikedSongsList])
				#bp()
			except Exception as e:
				print(e)
				errorUser[username]={"reason":str(e)}
			time.sleep(1)#request halt

csvFile.close()

with open('infoData.json','w') as outfile:
	json.dump(data,outfile)

with open('error.json','w') as outfile:
	json.dump(errorUser,outfile)
#save data into json file



