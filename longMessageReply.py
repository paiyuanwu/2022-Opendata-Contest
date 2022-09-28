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

def contactInfo():
    return TemplateSendMessage(
        alt_text='聯絡資訊',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://img.lovepik.com/free-png/20211201/lovepik-handsome-guy-png-image_401252085_wh1200.png',
                    title='勞利E指通負責人',
                    text='負責統籌開發項目',
                    actions=[
                        URIAction(
                            label='加入好友並尋求幫助',
                            uri='https://line.me/ti/p/iTQucXciCd'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://www.haushin.com.tw/files/LO100300-TSUMTSUM%E7%86%8A%E6%8A%B1%E5%93%A5%E9%80%A0%E5%9E%8B%E6%94%B6%E7%B4%8D%E6%AB%83-1.jpg',
                    title='勞利E指通小編',
                    text='及時為您提供最有效的諮詢服務',
                    actions=[
                        URIAction(
                            label='加入好友並尋求幫助',
                            uri='https://liff.line.me/1645278921-kWRPP32q/?accountId=700fmskf'
                        )
                    ]
                )
            ]
        )
    )

def locationInfo():
    return TemplateSendMessage(
        alt_text='鄰近辦事處',
        template=ButtonsTemplate(
            thumbnail_image_url='https://prairiedentalclinic.ca/wp-content/uploads/2021/08/Tumblr-Banner-14-1536x1195.png',
            title='鄰近辦事處',
            text="請選擇想查找鄰近辦事處的方式",
            actions=[
                URIAction(
                    label='GPS搜尋',
                    uri='line://nv/location',
                    text='GPS搜尋'
                ),
                MessageAction(
                    label='內政部勞工局服務據點',
                    text='各地辦事處'
                ),
            ]
        )
    )

def AIInfo():
    return TemplateSendMessage(
        alt_text='AI諮詢',
        template=ButtonsTemplate(
            thumbnail_image_url='https://prairiedentalclinic.ca/wp-content/uploads/2021/08/Tumblr-Banner-14-1536x1195.png',
            title='AI諮詢',
            text="請選擇想諮詢的類別",
            actions=[
                MessageAction(
                    label='法律與程序',
                    text='法律與程序'
                ),
                MessageAction(
                    label='勞保局行事曆與時程',
                    text='時程'
                ),
                MessageAction(
                    label='勞保與退休金',
                    text='勞保與退休金'
                ),
                MessageAction(
                    label='職災',
                    text='職災'
                ),
            ]
        )
    )

def EInfo():
    return TemplateSendMessage(
        alt_text='E化辦事處',
        template=ButtonsTemplate(
            thumbnail_image_url='https://img.lovepik.com/photo/50064/9004.jpg_wh860.jpg',
            title='身分認證和推播功能',
            text="請選擇身分認證方式或開啟推播功能",
            actions=[
                MessageAction(
                    label='影像辨識身分認證',
                    text='影像辨識'
                ),
                MessageAction(
                    label='OTP身分認證',
                    text='OTP'
                ),
                MessageAction(
                    label='推播功能',
                    text='推播功能'
                ),
            ]
        )
    )