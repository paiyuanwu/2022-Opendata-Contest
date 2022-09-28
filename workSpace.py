from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from linebot.models import *
line_bot_api = LineBotApi('2derjimPiD2zxmPb8PiushO3AUxG1o7KYnOXxMC19e0Xb4WMQWJht82IbFcUjoghB041nfYPp7HPFY1e7lklYRmKWrmu2H2qH39rqhvB5/SnsoDVDfo9F+EHgC/ktR7ztSvfQQjE9+EpygMGXjpKmgdB04t89/1O/w1cDnyilFU=')
#'你自己的token'
# 必須放上自己的Channel Secret
handler = WebhookHandler('b49f75466abc0de3f7c0a70651945152')#你自己的secret

class BaseWorkSpace:
    
    def __init__(self,event):
        self.event = event
        
    def action(self,info):
        match info["step"]:
            case 1:
                info = self.step1(info)
            case 2:
                info = self.step2(info)
            case 3:
                info = self.step3(info)
            case 4:
                info = self.step4(info)
            case 5:
                info = self.step5(info)
            case 6:
                info = self.step6(info)
            case _:
                line_bot_api.reply_message(self.event.reply_token, TextSendMessage('錯誤: action'))
        return info
    
    def step1(self,info):
        line_bot_api.reply_message(self.event.reply_token, TextSendMessage('錯誤: step1'))
        return info
    def step2(self,info):
        line_bot_api.reply_message(self.event.reply_token, TextSendMessage('錯誤: step2'))
        return info
    def step3(self,info):
        line_bot_api.reply_message(self.event.reply_token, TextSendMessage('錯誤: step3'))
        return info
    def step4(self,info):
        line_bot_api.reply_message(self.event.reply_token, TextSendMessage('錯誤: step4'))
        return info
    def step5(self,info):
        line_bot_api.reply_message(self.event.reply_token, TextSendMessage('錯誤: step5'))
        return info
    def step6(self,info):
        line_bot_api.reply_message(self.event.reply_token, TextSendMessage('錯誤: step6'))
        return info