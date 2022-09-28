from linebot import LineBotApi
from linebot.models import TextSendMessage
#import time

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('2derjimPiD2zxmPb8PiushO3AUxG1o7KYnOXxMC19e0Xb4WMQWJht82IbFcUjoghB041nfYPp7HPFY1e7lklYRmKWrmu2H2qH39rqhvB5/SnsoDVDfo9F+EHgC/ktR7ztSvfQQjE9+EpygMGXjpKmgdB04t89/1O/w1cDnyilFU=')
# 請填入您的ID
yourID = 'U713e92460c7e83f82e84ded750ac4d79'
# 主動推播訊息
line_bot_api.push_message(yourID,TextSendMessage(text='親愛的使用者您好，我們即將開始提供推送服務嘍！提供給您第一手的消息，保障您的權益'))
# 用迴圈推播訊息
###for i in [1,2,3,4,5]:
###    line_bot_api.push_message(yourID, 
###                              TextSendMessage(text='我們來倒數：'+str(i)))
###    time.sleep(1)
