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
import Database

line_bot_api = LineBotApi(
    '2derjimPiD2zxmPb8PiushO3AUxG1o7KYnOXxMC19e0Xb4WMQWJht82IbFcUjoghB041nfYPp7HPFY1e7lklYRmKWrmu2H2qH39rqhvB5/SnsoDVDfo9F+EHgC/ktR7ztSvfQQjE9+EpygMGXjpKmgdB04t89/1O/w1cDnyilFU=')
# '你自己的token'
# 必須放上自己的Channel Secret
handler = WebhookHandler('b49f75466abc0de3f7c0a70651945152')  # 你自己的secret


class PushMessage(BaseWorkSpace):

    def __init__(self, event):
        super().__init__(event)

    def step1(self,info):
        l = Database.data_get("推播名單")
        for i in l:
            line_bot_api.push_message(i[0],TextSendMessage(self.event.message.text))
        line_bot_api.reply_message(self.event.reply_token, TextSendMessage("尊貴的張漢宇大人，您的小弟們都已收到來自您的重要通知了"))
        info["step"] = 0
        return info
    