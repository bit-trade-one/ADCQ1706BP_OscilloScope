#!/usr/bin/python
#-*- coding:utf-8 -*-
#*******************************************************************
#  オシロスコープ　データ収集しグラフを作成する
#　約２秒周期でデーモンとして実行を繰り返す
#  収集データからグラフを作成しファイルとして保存する
#  毎回使用したリソースを解放する必要がある
#******************************************************************
from time import sleep
import subprocess as proc
import matplotlib as mplt
mplt.use("Agg")
import matplotlib.pyplot as plt
import serial

# ディレクトリ指定とファイル名指定
path = '/home/pi/Oscilloscope/'
graphfile = 'graph1.png'
filename = 'Hsync.txt'
filename1 = 'Chan.txt'
filename2 = 'Trig.txt'
filename3 = 'Rise.txt'

# 変数定義
data = []
Hsync = []
Chan = []
Trig = []
Rise = []
TrigPos = 2048

#**************** グラフ生成関数 ********************
def makeGraph():
	global data, Chan, Hsync, Rise, TrigPos
	samples = []
	for i in range(0, 2000):
		# data は bytes。各要素は int (0..255)
		lo = data[i*2 + 2] & 0x7F
		hi = data[i*2 + 3] & 0x1F
		samples.append((lo + (hi << 7)) - 2048)
	# グラフのインスタンス取得
	fig, ax1 = plt.subplots(1,1,figsize=(12, 6))
	# Y軸の目盛表示
	plt.ylim([-2048, 2047])           #ax1のY軸スケール指定
	plt.yticks([-2000,-1333,-667,0,667,1333,2000],[-1.5,-1,-0.5,0,0.5,1,1.5])
	ax1.set_ylabel('Volt', color='g')
	# 横軸の追加
	ax1.axhline(y=1333, color='gray', linestyle=':')
	ax1.axhline(y=667, color='gray', linestyle=':')
	ax1.axhline(y=0, color='gray', linestyle=':')
	ax1.axhline(y=-667, color='gray', linestyle=':')
	ax1.axhline(y=-1333, color='gray', linestyle=':')
	#トリガ位置ライン表示　立ち上がり時赤色、立ち下がり時青色
	if(Rise != '0'):
		ax1.axhline(y=TrigPos, color='red', linestyle=':')
	else:
		ax1.axhline(y=TrigPos, color='blue', linestyle=':')		
	#ラベル類表示、日本語の表示
	fontprop=mplt.font_manager.FontProperties(fname="/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf")
	#日本語タイトル
	ax1.set_title(u'オシロスコープ', fontsize=25, fontproperties=fontprop)
	#グラフの水平同期による変更
	if Hsync[0] == '0':			#0.25usecサンプル
		plt.xlim([0,200])		#横軸20倍に拡大
		#縦軸の表示　		
		for i in range(1, 10):
			ax1.axvline(x=20*i, color='gray', linestyle=':')
		#X軸目盛表示とスケール表示
		plt.xticks([0,20,40,60,80,100,120,140,160,180,200],[0,5,10,15,20,25,30,35,40,45,50])
		ax1.set_xlabel('5usec/dev', color='g') 
	elif Hsync[0] == '1':		#0.25usecサンプリング
		plt.xlim([0,400])		#横軸5倍に拡大
		#縦軸の表示
		for i in range(1, 10):
			ax1.axvline(x=40*i, color='gray', linestyle=':')
		#X軸目盛表示とスケール表示
		plt.xticks([0,40,80,120,160,200,240,280,320,360,400],[0,10,20,30,40,50,60,70,80,90,100])
		ax1.set_xlabel('10usec/dev', color='g') 
	elif Hsync[0] == '2':		#0.25usecサンプリング
		plt.xlim([0,2000])
		#縦軸の表示
		for i in range(1, 10):
			ax1.axvline(x=200*i, color='gray', linestyle=':')
		#X軸目盛表示とスケール表示
		plt.xticks([0,200,400,600,800,1000,1200,1400,1600,1800,2000],[0,50,100,150,200,250,300,350,400,450,500])
		ax1.set_xlabel('50usec/dev', color='g') 
	elif Hsync[0] == '3':		#0.5usecサンプルリング
		plt.xlim([0,1000])
		#縦軸の追加
		for i in range(1, 10):
			ax1.axvline(x=100*i, color='gray', linestyle=':')
		plt.xticks([0,100,200,300,400,500,600,700,800,900,1000],[0,100,200,300,400,500,600,700,800,900,1000])
		ax1.set_xlabel('100usec/dev', color='g') 
	elif Hsync[0] == '4':	#5usecサンプリング
		plt.xlim([0,2000])
		#縦軸の表示
		for i in range(1, 10):
			ax1.axvline(x=200*i, color='gray', linestyle=':')
		#X軸目盛表示とスケール表示
		plt.xticks([0,200,400,600,800,1000,1200,1400,1600,1800,2000],[0,1,2,3,4,5,6,7,8,9,10])
		ax1.set_xlabel('1msec/dev', color='g') 
	elif Hsync[0] == '5':		#10usecサンプリング
		plt.xlim([0,2000])
		#縦軸の表示
		for i in range(1, 10):
			ax1.axvline(x=200*i, color='gray', linestyle=':')
		#X軸目盛表示とスケール表示
		plt.xticks([0,200,400,600,800,1000,1200,1400,1600,1800,2000],[0,2,4,6,8,10,12,14,16,18,20])
		ax1.set_xlabel('2msec/dev', color='g') 
	elif Hsync[0] == '6':		#50usecサンプリング
		plt.xlim([0,2000])
		#縦軸の表示
		for i in range(1, 10):
			ax1.axvline(x=200*i, color='gray', linestyle=':')
		#X軸目盛表示とスケール表示
		plt.xticks([0,200,400,600,800,1000,1200,1400,1600,1800,2000],[0,10,20,30,40,50,60,70,80,90,100])
		ax1.set_xlabel('10msec/dev', color='g') 
	#グラフ描画
	if(Chan[0] == '1'):
		ax1.plot(samples, 'r')    #チャネル１の場合赤色
	elif(Chan[0] == '2'):
		ax1.plot(samples, 'b')	#チャネルの場合青色
	#グラフデータファイル保存
	fig.savefig(path+graphfile)	#グラフのファイル保存
	plt.close('all')			#matoplotのリソース解放

#*************** メイン関数　**********************
def main():
	global data, Hsync, Chan, Trig, TrigPos, Rise

	#シリアルインターフェース定義
	con=serial.Serial('/dev/ttyUSB0', 115200, timeout=2.0)
#	print con.portstr
	#*** 初期パラメータファイル作成 ****
	Hsync = '3'
	Chan = '1'
	Trig = '2048'
	Rise = '1'
	f = open(path+filename, 'w')
	f.write(Hsync)
	f.close()
	f = open(path+filename1, 'w')
	f.write(Chan)
	f.close()
	f = open(path+filename2, 'w')
	f.write(Trig)
	f.close()
	f = open(path+filename3, 'w')
	f.write(Rise)
	f.close()
	#************* データ取得とグラフ作成の永久ループ ******************
	try:
		while True:
			f = open(path+filename, 'r')		#水平同期設定読み込み
			Hsync = f.read(1)
			f.close()
			f = open(path+filename1, 'r')	#チャネル選択指定読み込み
			Chan = f.read(1)
			f.close()
			f = open(path+filename2, 'r')	#トリガレベル値読み込み
			Trig = f.read(4)
			f.close()
			f = open(path+filename3, 'r')	#立ち上がり、立ち下がり区別読み込み
			Rise = f.read(1)
			f.close()
			#トリガレベルを数字から数値に変換
			# TrigPos = int((ord(Trig[0])-0x30)*1000+(ord(Trig[1])-0x30)*100+(ord(Trig[2])-0x30)*10+(ord(Trig[3])-0x30))-2048
			TrigPos   = int((ord(Trig[0])-0x30)*1000 + (ord(Trig[1])-0x30)*100 + (ord(Trig[2])-0x30)*10 + (ord(Trig[3])-0x30)) - 2048

			#計測データ要求コマンド送信
			# con.write('ST'+Hsync[0]+Chan[0]+Trig[0]+Trig[1]+Trig[2]+Trig[3]+Rise[0]+'E')
			cmd = 'ST' + Hsync[0] + Chan[0] + Trig[0] + Trig[1] + Trig[2] + Trig[3] + Rise[0] + 'E'
			con.write(cmd.encode('ascii'))   # ← ここがポイント
			con.flush()
			#計測データ受信実行
			data = con.read(4003)
			if len(data) == 4003 and data.startswith(b'SM') and data.endswith(b'E'):
			# if(data[0]=='S')and(data[1]=='M')and(data[4002]=='E'):
				#グラフ作成実行
				makeGraph()
				#ファイルをコピーしファイル名変更　graph2の方を表示に使う
				proc.call("sudo cp /home/pi/Oscilloscope/graph1.png /home/pi/Oscilloscope/graph2.png",shell=True) 
			sleep(1.0);
	# エラー処理
	except Exception as e:
		print (str(e))
	print ("End")
#************* 起動確認 *****************
if __name__=='__main__':
	main()
