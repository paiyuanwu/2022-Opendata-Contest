from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from linebot.models import *
from workSpace import BaseWorkSpace
import random
line_bot_api = LineBotApi('2derjimPiD2zxmPb8PiushO3AUxG1o7KYnOXxMC19e0Xb4WMQWJht82IbFcUjoghB041nfYPp7HPFY1e7lklYRmKWrmu2H2qH39rqhvB5/SnsoDVDfo9F+EHgC/ktR7ztSvfQQjE9+EpygMGXjpKmgdB04t89/1O/w1cDnyilFU=')
#'你自己的token'
# 必須放上自己的Channel Secret
handler = WebhookHandler('b49f75466abc0de3f7c0a70651945152')#你自己的secret

class Booking(BaseWorkSpace):
    
    def __init__(self,event):
        super().__init__(event)
        
    def step1(self,info):
        info["time"] = self.event.message.text
        line_bot_api.reply_message(self.event.reply_token, TextSendMessage('請填寫預約辦事處:'))
        info["step"] = 2
        return info

    def step2(self, info):
        info["place"] = self.event.message.text
        line_bot_api.reply_message(self.event.reply_token, TextSendMessage('請填寫欲辦理事項:'))
        info["step"] = 3
        return info

    def step3(self,info):
        info["work"] = self.event.message.text
        line_bot_api.reply_message(self.event.reply_token, TextSendMessage('請填寫您的姓名:'))
        info["step"] = 4
        return info
    
    def step4(self,info):
        info["name"] = self.event.message.text
        line_bot_api.reply_message(self.event.reply_token, TextSendMessage('請填寫您的連絡電話:'))
        info["step"] = 5
        return info
    
    def step5(self,info):
        info["phone"] = self.event.message.text
        reply_arr = []
        num = self.number()
        reply_arr.append(TextSendMessage('完成預約，以下為預約資訊:\n時間: '+str(info["time"])+"\n辦事處: "+str(info["place"])+"\n辦理事項: "+str(info["work"])+"\n姓名: "+str(info["name"])+"\n電話: "+str(info["phone"])+"\n預約編號: "+num))
        reply_arr.append(TextSendMessage("感謝您的預約"))
        line_bot_api.reply_message(self.event.reply_token, reply_arr)
        info["step"] = 0
        return info

    def number(self):
        num=''
        for i in range(0,8):
            num += str(random.randint(0,9))
        return num