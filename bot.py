import time
import requests
import datetime
import json
from collections import namedtuple
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, URITemplateAction, PostbackTemplateAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent
    )

app = Flask(__name__)
now = datetime.datetime.now()
url = 'https://its.rvp.co.th/it/api/'

line_bot_api = LineBotApi('Py16F9GZePWwoBlq/r7aev30s9SUMYPsP9YAQpr4XBE2skelccadOvgDO8D04HMdNgmrVpu/N0edN8uBHVR36XlErDXbRFW2ODlr2yppKwSbKbhTTIPWe0sek7pzlvwySvDx04TSiPTTJDQAMrYjjgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('63bd28fd3a4fdadaa9655de644902fcc')

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route("/getResponse")
def hello():
     return "Hello World!"

@app.route("/webhook", methods=['POST'])
def webhook():

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
    # if request.method == 'POST':
    return 'OK'

    

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    if event.message.text == '!profile':
        profile = line_bot_api.get_profile(event.source.user_id)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(
                    text='Display name: '+ profile.display_name
                ),
                TextSendMessage(
                    text='Status message: ' + profile.status_message
                ),
                TextSendMessage(
                    text='Line id: '+ event.source.user_id
                )
            ]
        )
    elif event.message.text == '!show_groupid':
        if isinstance(event.source, SourceGroup):
            # print(event.source.type)
            # print(event.source.group_id)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='this group id is :'+event.source.group_id)
            )
    elif event.message.text == '!checkMonitor':
        try:
            response = requests.get(url+'Monitor/CheckAppsStatus')
            response = response.json() #to obj
            r = response[0] #to dict
            response_msg = r.get("BotMessage")
            if isinstance(event.source, SourceGroup):
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text= response_msg)
            )
        except:
            print('ERROR AT CONVERTS')
            if isinstance(event.source, SourceGroup):
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text = 'error please try again!')
                )

    else:
        if isinstance(event.source, SourceUser):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=event.message.text)
            )


# C8d731f5c4671277e13f9d49259281539 test group
# C66e0fc5a2d23607150d592d8396f4832 dev group
# Cad886fdebdc0a1de6eda6ad809a62a6a monitor group

testgroup = 'C8d731f5c4671277e13f9d49259281539'
selfid = 'Ucf3afd60234d7148a13aef99176b463c'
devgroup = 'C66e0fc5a2d23607150d592d8396f4832'
monitorgroup = 'Cad886fdebdc0a1de6eda6ad809a62a6a'
# Time = 35999



def getAppData():
    response = requests.post(url+'Monitor/CheckAppsStatus')
    response = response.json()
    response_json = response[0]
    return response_json

def getDbjobData():
    response = requests.post(url+'Monitor/CheckDbjobStatus')
    response = response.json()
    response_json = response[0]
    return response_json

def sendAppData(group_line):
    try:
        response = getAppData()
        response_check = response.get("Validate")
        response_msg = response.get("BotMessage")
        if(response_check != "T"):
            time.sleep(65)
            response = getAppData()
            response_check = response.get("Validate")
            response_msg = response.get("BotMessage")
            if(response_check == "T"):
                line_bot_api.push_message(group_line,
                TextSendMessage(text=response_msg))
                print('BotStatus:APPs OK')
                return True
            else:
                response_msg = "Cannot get data from API"
                line_bot_api.push_message(group_line,
                TextSendMessage(text=response_msg))
                print('BotStatus:APPs Cannot get data from API')
                return False
        else:
            line_bot_api.push_message(group_line,
            TextSendMessage(text=response_msg))
            print('BotStatus:APPs OK')
            return True
    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        error_status = template.format(type(ex).__name__, ex.args)
        print(error_status)
        line_bot_api.push_message(group_line,
        TextSendMessage(text='น้องแชปปี้ทำงานผิดพลาด กรุณาตรวจสอบภายหลัง :)'))
        return False

def sendDbjobData(group_line):
    try:
        response = getDbjobData()
        response_check = response.get("Validate")
        response_msg = response.get("BotMessage")
        if(response_check != "T"):
            time.sleep(65)
            response = getDbjobData()
            response_check = response.get("Validate")
            response_msg = response.get("BotMessage")
            if(response_check == "T"):
                line_bot_api.push_message(group_line,
                TextSendMessage(text=response_msg))
                print('BotStatus: DB JOBs OK')
                return True
            else:
                response_msg = "Cannot get data from API"
                line_bot_api.push_message(group_line,
                TextSendMessage(text=response_msg))
                print('BotStatus:DbJOB Cannot get data from API')
                return False
        else:
            line_bot_api.push_message(group_line,
            TextSendMessage(text=response_msg))
            print('BotStatus: DB JOBs OK')
            return True
    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        error_status = template.format(type(ex).__name__, ex.args)
        print(error_status)
        line_bot_api.push_message(group_line,
        TextSendMessage(text='น้องแชปปี้ทำงานผิดพลาด กรุณาตรวจสอบภายหลัง :)'))
        return False

try:
    groupLine = selfid
    appCheck = sendAppData(groupLine)
    dbCheck = sendDbjobData(groupLine)
    while(appCheck == False or dbCheck == False):
        time.sleep(300)
        #ถ้ายังมีข้อความใด False ให้ส่งข้อมูลใหม่ใน 5 นาทีถัดไป
        if(appCheck == False):
            appCheck = sendAppData(groupLine)
        if(dbCheck == False):
            dbCheck = sendDbjobData(groupLine)
except Exception as ex:
    template = "An exception of type {0} occured. Arguments:\n{1!r}"
    error_status = template.format(type(ex).__name__, ex.args)
    print(error_status)

raise RuntimeError('Not running with the Werkzeug Server') 
#เมื่อส่งข้อความเสร็จให้ส่ง error เพื่อปิดการทำงาน batch

if __name__ == "__main__":
    app.run()

