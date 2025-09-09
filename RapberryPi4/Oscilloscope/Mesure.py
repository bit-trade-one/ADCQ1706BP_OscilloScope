#!/usr/bin/python
#-*- coding:utf-8 -*-
#**********************************************************
#  オシロスコープ　Pythonマクロ関数群
#　パラメータのファイル保存とシャットダウン実行
#**********************************************************
from time import sleep
import webiopi
import subprocess as proc
import serial

#ディレクトリとファイル名宣言
path = '/home/pi/Oscilloscope/'
filename = 'Hsync.txt'
filename1 = 'Chan.txt'
filename2 = 'Trig.txt'
filename3 = 'Rise.txt'
#******** トリガー関数 デーモンとして起動　************
@webiopi.macro
def GetGraph():
	proc.call("sudo killall sudo", shell=True)	# 既存をクローズする
	proc.call("sudo python /home/pi/Oscilloscope/Gathering.py &", shell=True)
#******* 水平同期設定値保存 *********
@webiopi.macro
def SetHsync(para):
	try:
		f = open(path+filename, 'w')
		f.write(para)
		f.close()
	except KeyboardInterrupt:
		pass
#******** チャネル切り替え設定値保存 *****
@webiopi.macro
def SetChan(para):
	try:
		f = open(path+filename1, 'w')
		f.write(para)
		f.close()
	except KeyboardInterrupt:
		pass
#******** トリガレベル値保存 ********
@webiopi.macro
def SetTrig(para):
	try:
		f = open(path+filename2, 'w')
		f.write(para)
		f.close()
	except KeyboardInterrupt:
		pass
#******** トリガ向き保存 ********
@webiopi.macro
def SetRise(para):
	try:
		f = open(path+filename3, 'w')
		f.write(para)
		f.close()
	except KeyboardInterrupt:
		pass
#***** シャットダウン実行関数 *******
@webiopi.macro
def ShutCmd():
	proc.call("sudo killall sudo", shell=True)
	proc.call("sudo /sbin/shutdown -h now", shell=True)	
