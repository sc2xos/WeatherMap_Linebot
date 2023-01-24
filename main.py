#%%
import os
import sys
import urllib.request
from datetime import datetime,timezone,timedelta

from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.models import ImageSendMessage
from linebot.exceptions import LineBotApiError

import cv2
#%%時刻の取得
JST = timezone(timedelta(hours=+9), 'JST')
valid_time  = datetime.now(JST)
next_day =( (valid_time + timedelta(days=1))).isoformat()[8:10]
year = valid_time.isoformat()[2:4]
month = valid_time.isoformat()[5:7]
day = valid_time.isoformat()[8:10]
hour = valid_time.isoformat()[11:13]
print("########## Date : {} ##########".format(valid_time.isoformat()[0:16]))
#%%Define file name
wm = '{0}{1}{2}{3}.png'.format(year,month,day,hour)
wm24 = '{0}{1}{2}{3}.png'.format(year,month,next_day,'09')
wm48 = '{0}{1}{2}{3}.png'.format(year,month,next_day,'21')
send_image = "send_{0}{1}{2}{3}.png".format(year,month,day,hour)
#Define for LineAPI
access_token = "r6jN8HX4l+M5THeQNveYZttQwrW5h/4fLlRGWd9rcwOUlzHeDSNQrsXEBjWiVseWYgAngA1XwrX69mZruMXzz1jJt9mEP0c88nhjXezF8oa+qq0hdYUrM5jUEU8bOebhplLrU9iQt/G0OI5OUFAIvQdB04t89/1O/w1cDnyilFU="
line_bot_api = LineBotApi(access_token)
#Heroku
app_url = "https://wmlinebot.herokuapp.com"
#%%URLの定義
def define_url(hour):
    #hour = str(int(hour) - (int(hour) % 3)).zfill(2)
    URL = 'https://www.jma.go.jp/jp/g3/images/jp_c/{0}'.format(wm)
    URL24 = 'https://www.jma.go.jp/jp/g3/images/jp_c/24h/{0}'.format(wm24)
    URL48 = 'https://www.jma.go.jp/jp/g3/images/jp_c/48h/{0}'.format(wm48)
    return URL, URL24, URL48
#%%URLが有効化どうかのチェック
def UrlChecker(urlname00):
    try:
        res = urllib.request.urlopen(urlname00)
        un=res.geturl()
        res.close()
        if(un == urlname00):
            return 1
        else:
            return 0
        pass
    except:
        return 0
        pass
#%%天気図のダウンロード
def wm_download(url, title):
    print("Download from",url)
    try:
        urllib.request.urlopen(url)
        urllib.request.urlretrieve(url,title)
        print("Complete Download!")
    except urllib.error.HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
        sys.exit()
    except urllib.error.URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
        sys.exit()
#%%Botへのメッセージの送信
def send_text(message):
    try:
        line_bot_api.broadcast(TextSendMessage(text = message))
    except LineBotApiError as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error.message)
        print(e.error.details)

#%%Botへの画像の送信
def sending_image(image):
    #imageの送信
    image_message = ImageSendMessage(
        original_content_url = "{0}/{1}".format(app_url, image),
        preview_image_url = "{0}/{1}".format(app_url, image)
    )
    try:
        line_bot_api.broadcast(image_message)
    except LineBotApiError as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error.message)
        print(e.error.details)
##%%画像の結合
def image_concat():
    print("Concatenating Images")
    try:
        with open(wm, 'r') as f:
            im1 = cv2.imread(wm)
            im2 = cv2.imread(wm24)
            im3 = cv2.imread(wm48)
            im_h = cv2.hconcat([im1, im2, im3])
            cv2.imwrite(send_image, im_h)
            print("Complete Concatenation !")
            return True
    except FileNotFoundError as e:
        return False
    except IOError as e:
        return False

#%%
def main():
    URL, URL24, URL48 = define_url(hour)
    if(os.path.isfile(send_image) == False):
        wm_download(URL, wm)
        wm_download(URL24, wm24)
        wm_download(URL48, wm48)
        image_concat()
        send_text("https://www.jma.go.jp/jp/g3/")
        sending_image(send_image)
    else:
        print("Already Send Image")
        print("Main Process Skip !")
        sys.exit()
#%%
if __name__ == "__main__":
    if(hour == "09" or hour =="12" or hour == "15" or hour =="18" or hour == "21"):
        main()
    else:
        print("Out of Execution Time")
        print("End Process !")
        sys.exit()
#%%
