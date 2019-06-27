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
# now = datetime.datetime.now()
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
    return "Chappie Online !! ¯\_(ツ)_/¯"

@app.route("/webhook", methods=['POST'])
def webhook():

    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: "+ body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


testgroup = 'C8d731f5c4671277e13f9d49259281539'
devgroup = 'C66e0fc5a2d23607150d592d8396f4832'
monitorgroup = 'Cad886fdebdc0a1de6eda6ad809a62a6a'

def Notify_Dev():
    response = requests.post(url+'Monitor/CheckMonitorNotification')
    response = response.json()
    response_json = response[0]
    return response_json

def send_Notify_Dev(group_line):
    try:
        response = Notify_Dev()
        response_check = response.get("Validate")
        response_msg = response.get("BotMessage")
        if(response_check != "T"):
            time.sleep(65)
            response = Notify_Dev()
            response_check = response.get("Validate")
            response_msg = response.get("BotMessage")
            if(response_check == "T"):
                line_bot_api.push_message(group_line,
                TextSendMessage(text = response_msg))
                print('BotStatus: Send done')
                return True
            else:
                response_msg = "Cannot get data from API"
                line_bot_api.push_message(group_line,
                TextSendMessage(text=response_msg))
                print('BotStatus: Bot Cannot get data from API')
                return False
        else:
            line_bot_api.push_message(group_line,
            TextSendMessage(text=response_msg))
            print('BotStatus: Send done')
            return True
    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        error_status = template.format(type(ex).__name__, ex.args)
        print(error_status)
        line_bot_api.push_message(group_line,
        TextSendMessage(text='น้องแชปปี้ทำงานผิดพลาด กรุณาตรวจสอบภายหลัง :)'))
        return False

try:
    groupLine = testgroup
    notifyCheck = send_Notify_Dev(groupLine)
    while(notifyCheck == False):
        time.sleep(300)
        if(notifyCheck == False):
            notifyCheck = Notify_Dev()
except Exception as ex:
    template = "An exception of type {0} occured. Arguments:\n{1!r}"
    error_status = template.format(type(ex).__name__, ex.args)
    print(error_status)

raise RuntimeError('Not running with the Werkzeug Server')

if __name__ == "__main__":
    app.run()

