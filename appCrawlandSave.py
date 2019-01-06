#!/usr/bin/env python

import os
import time
import datetime
import subprocess

dumpDir="/sdcard/neteasePeopleData/"
prefix="people"
i=2826;#start number
while 1:
	#print(str(datetime.datetime.now())+"*********start No."+str(i)+" crawling**********")
	gotoh5=os.system("adb shell input tap 139 1630")
	time.sleep(15)
	#check if in html page
	position=subprocess.check_output("adb shell dumpsys window windows | grep -E 'mCurrentFocus'", shell=True)
	if "com.netease.cloudmusic.activity.H5CustomViewActivity" not in position:
		print("html5 fail to start")
		break
	match=os.system("adb shell input tap 530 724")

	time.sleep(15)
	#save current xml
	save=os.system("adb shell uiautomator dump "+dumpDir+prefix+str(i)+".xml")
	#print(str(datetime.datetime.now())+" Successfully saved No."+str(i)+"data to "+dumpDir+prefix+str(i)+".xml")
	back=os.system("adb shell input keyevent 4")
	i=i+1