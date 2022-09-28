# -*- coding: utf-8 -* 
#載入LineBot所需要的套件
from flask import Flask, request, abort

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
import re
from infoProcess import whichJob
import longMessageReply
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('2derjimPiD2zxmPb8PiushO3AUxG1o7KYnOXxMC19e0Xb4WMQWJht82IbFcUjoghB041nfYPp7HPFY1e7lklYRmKWrmu2H2qH39rqhvB5/SnsoDVDfo9F+EHgC/ktR7ztSvfQQjE9+EpygMGXjpKmgdB04t89/1O/w1cDnyilFU=')
#'你自己的token'
# 必須放上自己的Channel Secret
handler = WebhookHandler('b49f75466abc0de3f7c0a70651945152')#你自己的secret

#line_bot_api.push_message('U713e92460c7e83f82e84ded750ac4d79', TextSendMessage(text='你可以開始了'))#'你自己的ID'
userTable = []

def userInfoInit():
    return {
        "userID": 0,
        "workSpace": 0,
        "step": 0,
        "time": 0,
        "place": 0,
        'work' : 0,
        "name": 0,
        "phone": 0,
        "AI": 0,
        "lat" : 0,#緯度
        "long" : 0,#經度
        "au" : 0,
        'service' : 0,
    }
# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    userID = event.source.user_id
    userInfo = userInfoInit()
    userInfo["userID"] = userID

    newUser = True
    for info in userTable:
        if userID == info["userID"]:
            userInfo = whichJob(info,event)
            if userInfo["step"] == 0:
                userTable.remove(info)
            else:
                info = userInfo
            newUser = False
            break

    if newUser:
        message = event.message.text

        if re.match('AI',message):
            buttons_template_message = longMessageReply.AIInfo()
            line_bot_api.reply_message(event.reply_token, buttons_template_message)
            userInfo["workSpace"] = 1
            userInfo["step"] = 1
        elif re.match('線上預約',message):
            userInfo["workSpace"] = 3
            userInfo["step"] = 1
            line_bot_api.reply_message(event.reply_token,TextSendMessage('請填寫預約時間:'))
        elif re.match('線上客服',message):
            carousel_template_message = longMessageReply.contactInfo()
            line_bot_api.reply_message(event.reply_token, carousel_template_message)
        elif re.match('鄰近辦事處',message):
            buttons_template_message = longMessageReply.locationInfo()
            line_bot_api.reply_message(event.reply_token, buttons_template_message)
            userInfo["workSpace"] = 4
            userInfo["step"] = 1
        elif re.match('E化辦事處',message):
            buttons_template_message =longMessageReply.EInfo()
            line_bot_api.reply_message(event.reply_token, buttons_template_message)
            userInfo["workSpace"] = 2
            userInfo["step"] = 1
        elif re.match('推',message) and userID == "U4ed062587511d7fb25c211a84114013f":
            line_bot_api.reply_message(event.reply_token, TextSendMessage("尊貴的張漢宇大人，請問您打算推播甚麼消息給您的小弟們?"))
            userInfo["workSpace"] = 5
            userInfo["step"] = 1
        else :
            line_bot_api.reply_message(event.reply_token,TextSendMessage("無效輸入"))
        if userInfo["step"] != 0:
            userTable.append(userInfo)

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    # 獲取使用者的經緯度
    userID = event.source.user_id
    userInfo = userInfoInit()
    userInfo["userID"] = userID

    for info in userTable:
        if userID == info["userID"]:
            if info["workSpace"] == 4 and info["step"] == 1:
                userInfo = whichJob(info,event)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage('訊息格式錯誤!'))
                userTable.remove(info)
                return
            if userInfo["step"] == 0:
                userTable.remove(info)
            else:
                info = userInfo
            newUser = False
            break

@handler.add(MessageEvent, message = ImageMessage)
def handle_location_message(event):
    userID = event.source.user_id
    userInfo = userInfoInit()
    userInfo["userID"] = userID
    
    for info in userTable:
        if userID == info["userID"]:
            if (info["workSpace"] == 2 and info["step"] == 2) or (info["workSpace"] == 2 and info["step"] == 5):
                userInfo = whichJob(info,event)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage('訊息格式錯誤!'))
                userTable.remove(info)
                return
            if userInfo["step"] == 0:
                userTable.remove(info)
            else:
                info = userInfo
            newUser = False
            break


@handler.add(MessageEvent, message=FileMessage)
def handle_location_message(event):
    userID = event.source.user_id
    userInfo = userInfoInit()
    userInfo["userID"] = userID

    for info in userTable:
        if userID == info["userID"]:
            if info["workSpace"] == 2 and info["step"] == 5:
                userInfo = whichJob(info, event)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage('訊息格式錯誤!'))
                userTable.remove(info)
                return
            if userInfo["step"] == 0:
                userTable.remove(info)
            else:
                info = userInfo
            newUser = False
            break

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)