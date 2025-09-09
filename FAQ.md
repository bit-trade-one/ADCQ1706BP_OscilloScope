# ADCQ1706BPRE-USBオシロスコープ よくある質問

## Q. Raspberry Pi 4で動作しますか？
 
### A. サンプルアプリの修正が必要になります
Raspberry Pi 4のRaspberry Pi OSの環境で動作させるには、以下の修正が必要となります。
- Python2環境からPython3環境への移行  
文字列型の違い等を修正する必要gああります。
- 必要なモジュールやファイルのインストール（matplotlib、フォント等）
```
sudo apt install -y python3-matplotlib
sudo apt install fonts-ipafont fonts-ipaexfont
```
- GPIOに互換性がないため、WebIOPIの動作に制限があります。本製品をRaspberry Pi 4で使う場合には付属のUSBシリアル変換モジュールをご使用ください。  
この場合、シリアルのデバイス名は「/dev/ttyUSB0」等の名称となります。
- Raspberry Pi 4BにRaspberry Pi OS(64-bit） 2025-05-13をインストールした環境で動作するRaspberry Piアプリケーションを参考にしてください。  
[Raspberry Pi 4 サンプルアプリ](https://github.com/bit-trade-one/ADCQ1706BP_OscilloScope/tree/master/RapberryPi4/Oscilloscope)

## Q. WebIOPIがインストールできない
 
### A. 雑誌記事のテキストに誤記と全角スペースが含まれています。下記のコマンドを実行してください。
```
sudo wget https://sourceforge.net/projects/webiopi/files/WebIOPi-0.7.1.tar.gz
sudo tar xvzf WebIOPi-0.7.1.tar.gz
cd WebIOPi-0.7.1/
wget https://raw.githubusercontent.com/doublebind/raspi/master/webiopi-pi2bplus.patch
patch -p1 -i webiopi-pi2bplus.patch
sudo ./setup.sh
 ```
## Q. Webiopiのconfigファイル変更が反映されない
 
### A. 解凍したconfigファイルではなく、/etc/webiopi/configを修正してください。
また、解凍したconfigファイルの以下の部分を修正してください。  
　誤：doc-root = /home/pi/DMM  
　正；doc-root = /home/pi/Oscilloscope  

## Q. Raspberry Piのすべてのユーザで動作しますか？
 
### A. サンプルアプリはuser:piで動作するように設定されています。  
他のユーザで動作させる場合は、すべてのスクリプト、および設定ファイルの/home/piの部分を修正してください。


## Q:Windows用のアプリケーションログ出力はどのような間隔で出力されているのでしょうか？

### A:以下のような出力になっております。  
  
１．アプリから基板に対してデータ取得要求を出します。  
２．基板は水平時間軸の設定に応じた周期でAD変換を行いデータを取得します。  
　　8ksps：2msec/div,5ms/div,10ms/div  
　　4ksps：25ms/div  
　　2ksps：50ms/div  
　　1ksps：100ms/div  
３．基板は、データが2000データ取得完了後にアプリ側にデータを送信します。  
４．アプリ側は取得した2000データをログに出力します。  
1～４を繰り返して計測データを出力していますが、  
AD変換が終わって次のデータ取得要求によってAD変換を開始するまでに  
間隔が空いてしまいますのでトータルのデータでサンプリング周期を計算すると一致しません。  
2000データ毎には、指定のサンプリング周期にはなっていますが、  
2000データ毎の区切り部分では計測データは連続しておらず多少の間隔が空いております。

## Q. 基板上のジャンパの詳細について

### A:以下のドキュメントを参照してください。
[ADCQ1706B_ジャンパーピンについて_2020-11-19](
https://github.com/bit-trade-one/ADCQ1706BP_OscilloScope/blob/master/ADCQ1706B_%E3%82%B8%E3%83%A3%E3%83%B3%E3%83%91%E3%83%BC%E3%83%94%E3%83%B3%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6_2020-11-19.pdf)