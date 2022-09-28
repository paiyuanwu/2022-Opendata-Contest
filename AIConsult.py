from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from linebot.models import *
from workSpace import BaseWorkSpace
import jieba
from Database import data_get
import re
line_bot_api = LineBotApi(
    '2derjimPiD2zxmPb8PiushO3AUxG1o7KYnOXxMC19e0Xb4WMQWJht82IbFcUjoghB041nfYPp7HPFY1e7lklYRmKWrmu2H2qH39rqhvB5/SnsoDVDfo9F+EHgC/ktR7ztSvfQQjE9+EpygMGXjpKmgdB04t89/1O/w1cDnyilFU=')
# '你自己的token'
# 必須放上自己的Channel Secret
handler = WebhookHandler('b49f75466abc0de3f7c0a70651945152')  # 你自己的secret


class AI(BaseWorkSpace):

    def __init__(self, event):
        self.keyWord = []
        jieba.load_userdict('mydict.txt')
        super().__init__(event)

    def step1(self, info):
        info["AI"] = self.event.message.text
        if not self.check(info):
            line_bot_api.reply_message(self.event.reply_token, TextSendMessage('無效的輸入!請重新選擇'))
            info["step"] = 0
            return info
        line_bot_api.reply_message(self.event.reply_token, TextSendMessage('請告訴我您的問題'))
        info["step"] = 2
        return info
    
    def check(self,info):
        work = ["法律與程序","時程","勞保與退休金","職災"]
        for w in work:
            if info["AI"] == w:
                return True
        return False
    
    def step2(self,info):
        self.keywordProcess()
        data = []
        inf = []
        if info["AI"] == "法律與程序":
            inf = self.law()
        elif info["AI"] == "時程":
            inf = self.calendar()
        elif info["AI"] == "勞保與退休金":
            inf = self.insurance()
        elif info["AI"] == "職災":
            inf = self.disaster()
        else:
            line_bot_api.reply_message(self.event.reply_token, TextSendMessage('奇怪的BUG!!!'))
            info["step"] = 0
            return info
        
        for i in inf:
            data.append(data_get(i))
        data = self.findWord(data)
        reply_arr = []
        reply_arr.append(TextSendMessage("已為您找尋最相關的資訊:"))
        for i in range(0,len(data)):
            s=''
            for j in range(0,len(data[i])):
                if data[i][j] != '':
                    s += data[i][j]
                    if j != len(data[i]) - 1 and s != '':
                        s += '\n'
            if i < 4 and s != '':
                reply_arr.append(TextSendMessage(s))
        print(self.keyWord)
        if "勞保" in self.keyWord:
            reply_arr = InData()
        line_bot_api.reply_message(self.event.reply_token,reply_arr)
        info["step"] = 0
        return info
    
    def law(self):
        return ['災區受災勞工保險與就業保險被保險人保險費支應及傷病給付辦法','勞、就保投保單位申請補發保險費繳款單之方式','勞工保險法令規章','勞工保險被保險人因執行職務而致傷病審查準則','勞工退休金提停繳申報作業','勞工退休金請領程序']
    def calendar(self):
        return ['人民申請案件時限一覽表','勞保局行事曆']
    def insurance(self):
        return ['人民申請案件時限一覽表', '外國籍員工參加勞工保險應檢附證明文件一覽表', '申請墊償應備文件', '災區受災勞工保險與就業保險被保險人保險費支應及傷病給付辦法',
    '保險費負擔比例一覽表', '勞、就保投保單位申請補發保險費繳款單之方式', '勞工保險被保險人因執行職務而致傷病審查準則', '勞工退休金提停繳申報作業', '勞工退休金請領程序', '勞工退休金繳款單補單方式']

    
    def disaster(self):
        return ['勞工保險失能給付標準及同標準第三條附表','勞工保險被保險人因執行職務而致傷病審查準則']
        
    def keywordProcess(self):
        self.keyWord = jieba.lcut(self.event.message.text)
    
    def findWord(self,data):
        mostWord = 0
        d = []
        for i in range(0,len(data)):
            for j in range(0,len(data[i])):
                count = 0
                for k in range(0,len(data[i][j])):
                    w = jieba.lcut(data[i][j][k])
                    count += self.count(w)
                if count == mostWord:
                    d.append(data[i][j])
                elif count > mostWord:
                    mostWord = count
                    d.clear()
                    d.append(data[i][j])
        print(mostWord)
        return d
    def count(self,data):
        c = 0
        a = [0]*len(self.keyWord)
        for i in data:
            for j in range(len(self.keyWord)):
                if self.keyWord[j] == i and a[j] == 0:
                    c += 1
                    a[j] = 1
        return c
def InData():
    return [TextSendMessage("已為您找尋最相關的資訊:"),
            TextSendMessage("勞保新投保/勞退開戶提繳\n應備申請文件: 1-1-2僅辦理勞保新投保及勞退開戶提繳者1.投保申請書(勞保、健保及勞退3合1表格）\n申請費用: 0元\n受理單位: 納保組(新投保科)\n審查單位: 納保組（新投保科）勞工退休金組\n作業天數: 約6天\n備註: 自寄送文件之當日投保生效"),
            TextSendMessage("勞保新投保/勞退開戶提繳\n應備申請文件: 1-1-2僅辦理勞保新投保及勞退開戶提繳者2.加保申報表(勞保及勞退2合1表格）\n申請費用: 0元\n受理單位: 納保組(新投保科)\n審查單位: 納保組（新投保科）勞工退休金組\n作業天數: 約6天\n備註: 自寄送文件之當日投保生效"),
            TextSendMessage("勞保新投保/勞退開戶提繳\n應備申請文件: 1-1-2僅辦理勞保新投保及勞退開戶提繳者3.負責人身分證正背面影本\n申請費用: 0元\n受理單位: 納保組(新投保科)\n審查單位: 納保組（新投保科）勞工退休金組\n作業天數: 約6天\n備註: 自寄送文件之當日投保生效"),
            TextSendMessage("勞保新投保/勞退開戶提繳\n應備申請文件: 1-1-2僅辦理勞保新投保及勞退開戶提繳者4.主管機關核發之證件影本，例如：工廠、公司、商業登記證明文件、立案或登記證明書等\n申請費用: 0元\n受理單位: 納保組(新投保科)\n審查單位: 納保組（新投保科）勞工退休金組\n作業天數: 約6天\n備註: 自寄送文件之當日投保生效")]