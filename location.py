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
import math
from math import radians, cos, sin, asin, sqrt
from Database import data_get
import re
import sys
GOOGLE_API_KEY = 'AIzaSyABEVnltET6Zd6EjiJHYtPcj1pJAL5N_C0'
line_bot_api = LineBotApi('2derjimPiD2zxmPb8PiushO3AUxG1o7KYnOXxMC19e0Xb4WMQWJht82IbFcUjoghB041nfYPp7HPFY1e7lklYRmKWrmu2H2qH39rqhvB5/SnsoDVDfo9F+EHgC/ktR7ztSvfQQjE9+EpygMGXjpKmgdB04t89/1O/w1cDnyilFU=')
#'你自己的token'
# 必須放上自己的Channel Secret
handler = WebhookHandler('b49f75466abc0de3f7c0a70651945152')#你自己的secret

class Location(BaseWorkSpace):
    
    def __init__(self,event):
        super().__init__(event)
    
    def dist(self,info, long, lat):
        p = math.pi/180
        a = 0.5 - cos((lat-info['lat'])*p)/2 + cos(info['lat']*p) * \
            cos(lat*p) * (1-cos((long-info['long'])*p))/2
        print([info['lat'], info['long'], lat, long])
        return 12742 * asin(sqrt(a))
          
    def step1(self,info):
        
        data=data_get("勞保局各地辦事處")
        if self.event.message.type == "location":
            info=self.step3(info)

        elif self.event.message.text == "各地辦事處":
            line_bot_api.reply_message(self.event.reply_token, TextSendMessage('請輸入您想搜尋的行政區：'))
            info["step"] = 2
        else:
            line_bot_api.reply_message(self.event.reply_token, TextSendMessage('輸入無法辨識，請重新輸入！'))
            info["step"] = 0
    
        return info
    
    def step2(self,info):

        fid=self.event.message.text
        print(type(fid))
        data=data_get("勞保局各地辦事處")
        reply_arr = []
        reply_arr.append(TextSendMessage("以下為您欲搜尋的鄰近辦事處"))
        for i in range(0,len(data)):
            if fid in data[i][0]:
                 
                 reply_arr.append(TextSendMessage("辦事處： "+str(data[i][0])+"\n辦事處地址： "+str(data[i][1])+"\n辦事處電話： "+str(data[i][4])+"\n辦事處櫃檯服務時間： "+str(data[i][5])+"\n辦事處電話服務時間： "+str(data[i][6])))
        line_bot_api.reply_message(self.event.reply_token, reply_arr)
        info["step"] = 0
        return info

    def step3(self,info):    

        info["long"]=self.event.message.longitude
        info["lat"]=self.event.message.latitude
        data=data_get("勞保局各地辦事處")
        street=sys.float_info.max
        place=0
        for i in range(0,len(data)):
            lat= float(data[i][2])
            long=float(data[i][3])
            temp=self.dist(info, long, lat)
            if temp<street:
                    street=temp
                    place=i
        map_url = "https://www.google.com/maps/search/?api=1&query={},{}&query_place_id={}".format(float(data[place][2]),float(data[place][3]),data[place][0])
        buttons_template_message = TemplateSendMessage(
        alt_text='鄰近辦事處',
        template=ButtonsTemplate(
                thumbnail_image_url='https://download.logo.wine/logo/Google_Maps/Google_Maps-Logo.wine.png',
                title='鄰近辦事處',
                text="以下為您的鄰近辦事處",
                actions=[
                    URITemplateAction(
                        label='前往地圖',
                        uri=map_url
                    ),
                ]
            )
        )
        line_bot_api.reply_message(self.event.reply_token, buttons_template_message)
        info["step"] = 0
        return info
        


