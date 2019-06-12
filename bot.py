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

#chappie
#line_bot_api = LineBotApi('Py16F9GZePWwoBlq/r7aev30s9SUMYPsP9YAQpr4XBE2skelccadOvgDO8D04HMdNgmrVpu/N0edN8uBHVR36XlErDXbRFW2ODlr2yppKwSbKbhTTIPWe0sek7pzlvwySvDx04TSiPTTJDQAMrYjjgdB04t89/1O/w1cDnyilFU=')
#khun_sinmai
line_bot_api = LineBotApi('B7+XD/E492NrBIx9nHNpOwBdTbQ9ZNoayiOKD1ZLZvOqE5QATL9fNzKLy2NyvN0wHpmw3MmZDDj+8N81w8ckhLeE5/Fou1RW5ngnVJQQGlGg2XpP5nptvR1+jYFH2bYOnf5nR/2wJ5RkghN0It2n1QdB04t89/1O/w1cDnyilFU=')

#chappie
#handler = WebhookHandler('63bd28fd3a4fdadaa9655de644902fcc')
#khun_sinmai
handler = WebhookHandler('1271b23fb3f7217041dcaa37548f7bdd')

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
                    text='line_id: ' + event.source.user_id
                )
            ]
        )
    elif event.message.text == '!show_groupid':
        if isinstance(event.source, SourceGroup):
            # print(event.source.type)
            # print(event.source.group_id)
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text='this group id is :'+event.source.group_id),
                    TextSendMessage(text='your id is :'+event.source.user_id)
                ]
            )
    elif event.message.text == '!checkMonitor':
        response = requests.get(url+'Monitor/CheckAppsStatus')
        response = response.json() #to obj
        r = response[0] #to dict
        response_msg = r.get("BotMessage")
        try:
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


#C8d731f5c4671277e13f9d49259281539 test group
#C66e0fc5a2d23607150d592d8396f4832 dev group

# testgroup = 'C8d731f5c4671277e13f9d49259281539'
# devgroup = 'C66e0fc5a2d23607150d592d8396f4832'
# # Time = 35999

# try:
#     response = requests.post(url+'Monitor/CheckAppsStatus')
#     response = response.json()
#     r = response[0]
#     response_msg = r.get("BotMessage")
#     line_bot_api.push_message(devgroup,
#     TextSendMessage(text=response_msg))
#     print('BotStatus:APPs OK')
# except:
#     try:
#         response = requests.post(url+'Monitor/CheckAppsStatus')
#         response = response.json()
#         r = response[0]
#         response_msg = r.get("BotMessage")
#         line_bot_api.push_message(devgroup,
#         TextSendMessage(text=response_msg))
#         print('BotStatus: OK')
#     except Exception as ex:
#         template = "An exception of type {0} occured. Arguments:\n{1!r}"
#         error_status = template.format(type(ex).__name__, ex.args)
#         print(error_status)
#         line_bot_api.push_message(devgroup,
#         TextSendMessage(text='น้องแชปปี้ทำงานผิดพลาด กรุณาตรวจสอบภายหลัง'))


# try:
#     response = requests.post(url+'Monitor/CheckDbjobStatus')
#     response = response.json()
#     r = response[0]
#     response_msg = r.get("BotMessage")
#     line_bot_api.push_message(devgroup,
#     TextSendMessage(text=response_msg))
#     print('BotStatus: DB JOBs OK')
# except:
#     try:
#         response = requests.post(url+'Monitor/CheckDbjobStatus')
#         response = response.json()
#         r = response[0]
#         response_msg = r.get("BotMessage")
#         line_bot_api.push_message(devgroup,
#         TextSendMessage(text=response_msg))
#         print('BotStatus: DB JOBs OK')
#     except Exception as ex:
#         template = "An exception of type {0} occured. Arguments:\n{1!r}"
#         error_status = template.format(type(ex).__name__, ex.args)
#         print(error_status)
#         line_bot_api.push_message(devgroup,
#         TextSendMessage(text='น้องแชปปี้ทำงานผิดพลาด กรุณาตรวจสอบภายหลัง'))

# raise RuntimeError('Not running with the Werkzeug Server')


if __name__ == "__main__":
    app.run()

