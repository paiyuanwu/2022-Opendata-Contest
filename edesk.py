from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError)
    
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    TemplateSendMessage, ButtonsTemplate, URITemplateAction,
)
from linebot.models import *
from linebot.models import *

from workSpace import BaseWorkSpace
from Database import (data_get, data_insert ,data_del)
import re
import sys
GOOGLE_API_KEY = 'AIzaSyABEVnltET6Zd6EjiJHYtPcj1pJAL5N_C0'
line_bot_api = LineBotApi('2derjimPiD2zxmPb8PiushO3AUxG1o7KYnOXxMC19e0Xb4WMQWJht82IbFcUjoghB041nfYPp7HPFY1e7lklYRmKWrmu2H2qH39rqhvB5/SnsoDVDfo9F+EHgC/ktR7ztSvfQQjE9+EpygMGXjpKmgdB04t89/1O/w1cDnyilFU=')
#'你自己的token'
# 必須放上自己的Channel Secret
handler = WebhookHandler('b49f75466abc0de3f7c0a70651945152')#你自己的secret

class Edesk(BaseWorkSpace):
    
    def __init__(self,event):
        super().__init__(event)
    
          
    def step1(self,info):
        if  self.event.message.text == "影像辨識":
            line_bot_api.reply_message(self.event.reply_token, TextSendMessage('請傳送身分證照片：'))
            info["au"] = 1
        elif self.event.message.text == "OTP":
            line_bot_api.reply_message(self.event.reply_token, TextSendMessage('請輸入您的手機號碼：'))
            info["au"] = 2
        elif self.event.message.text == "推播功能":
            l = data_get("推播名單")
            print(l)
            if not (self.event.source.user_id,) in l:
                print(self.event.source.user_id)
                print(type(self.event.source.user_id))
                data_insert("推播名單",[(self.event.source.user_id,)])
                line_bot_api.reply_message(self.event.reply_token,TextSendMessage('已開啟自動化推播功能，若要關閉此功能，請再次選擇「E化辦事處->推播功能」'))
            else:
                data_del("推播名單","id",self.event.source.user_id)
                line_bot_api.reply_message(self.event.reply_token, TextSendMessage('已關閉自動化推播功能，若要再次開起此功能，請再次選擇「E化辦事處->推播功能」'))
            info["step"] = 0
            return info
        info["step"] = 2
        return info

    
    def step2(self,info):
        if info["au"] == 1:
            self.step3(info)
        elif info["au"] == 2:
            line_bot_api.reply_message(self.event.reply_token, TextSendMessage('已寄送OTP驗證碼，請輸入OTP簡訊密碼：'))
            info["step"] = 3

        else :
            line_bot_api.reply_message(self.event.reply_token, TextSendMessage('怪怪的...'))
            info["step"] = 0
            return info
        

        return info

    def step3(self,info):    
        reply_arr = []
        reply_arr.append(TextSendMessage('驗證成功'))
         #self.OTP()
        buttons_template_message = TemplateSendMessage(
            alt_text='E化辦事處',
            template=ButtonsTemplate(
                thumbnail_image_url='https://www.crazyvector.com/wp-content/uploads/2018/11/Free-Office-Icons-21.jpg',
                title='E化辦事處服務項目',
                text="請選擇服務項目",
                actions=[
                    MessageAction(
                        label='相關費用繳納',
                        text='繳費'
                    ),
                    MessageAction(
                        label='繳交退休金申請書',
                        text='繳交退休金申請書'
                    ),
                ]
            )
        )
        reply_arr.append(buttons_template_message)
        line_bot_api.reply_message(self.event.reply_token, reply_arr)
        info["step"] = 4
        return info
     
    def step4(self,info):
        if self.event.message.text == "繳費":    
            reply_arr = []
            buttons_template_message = TemplateSendMessage(
                alt_text='繳費用',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://png.pngtree.com/png-vector/20190727/ourlarge/pngtree-business-work-to-do-list-png-image_1635099.jpg',
                    title='繳費項目',
                    text="請選擇欲繳費項目",
                    actions=[
                        MessageAction(
                            label='勞(就、職)保保險費網路繳費',
                            text='勞(就、職)保'
                        ),
                        MessageAction(
                            label='勞工退休金網路繳費',
                            text='勞工退休金'
                        ),
                        MessageAction(
                            label='國民年金保險費網路繳費',
                            text='國民年金'
                        ),
                    ]
                )
            )
            reply_arr.append(buttons_template_message)
            line_bot_api.reply_message(self.event.reply_token, reply_arr)
            info['service'] = 1
            info["step"] = 5
        elif self.event.message.text == '繳交退休金申請書':
            line_bot_api.reply_message(self.event.reply_token, TextSendMessage('請上傳您的申請文件'))
            info['service'] = 2
            info["step"] = 5
        else:
            info["step"] = 0
        return info

    def step5(self,info):
        if info['service'] == 1:
            reply_arr = []
            buttons_template_message = TemplateSendMessage(
                alt_text='繳費用',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://img.ixintu.com/download/jpg/202001/2d9b491fe3208020b2980da094729952.jpg!con',
                    title='繳費方式',
                    text="請選擇付款方式",
                    actions=[
                        MessageAction(
                            label='銀行轉帳',
                            text='銀行轉帳',
                        ),
                        URIAction(
                            label='條碼掃描',
                            uri='line://nv/QRCodeReader',
                            text='GPS搜尋'
                        ),
                    ]
                )
            )
            reply_arr.append(buttons_template_message)
            line_bot_api.reply_message(self.event.reply_token, reply_arr)
            info["step"] = 6

        elif info['service'] == 2:
            line_bot_api.reply_message(self.event.reply_token, TextSendMessage('已收到您的文件'))
            info["step"] = 0
        return info
    def step6(self,info):
        if self.event.message.text == "銀行轉帳":
            reply_arr = []
            reply_arr.append(TextSendMessage('請將指定金額轉至下方之指定帳戶\n金額: 1054\n帳號: 496582 678404\n感謝您使用本服務'))
            line_bot_api.reply_message(self.event.reply_token, reply_arr)
        else :
            line_bot_api.reply_message(self.event.reply_token, TextSendMessage('錯誤訊息'))
        info["step"] = 0
        return info