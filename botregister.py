#!/usr/bin/ python

import os, sys
import time
import requests
import datetime
import json
import string
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
#line_bot_api = LineBotApi('B7+XD/E492NrBIx9nHNpOwBdTbQ9ZNoayiOKD1ZLZvOqE5QATL9fNzKLy2NyvN0wHpmw3MmZDDj+8N81w8ckhLeE5/Fou1RW5ngnVJQQGlGg2XpP5nptvR1+jYFH2bYOnf5nR/2wJ5RkghN0It2n1QdB04t89/1O/w1cDnyilFU=')
#rvp
accesstoken = 'x+slzRC7b27fT1CbP0n1W4jsfniVlpWaw2hHDrUiBhbLxZ9eNqcmsplXgO4G1FsHLWPcotN8F6uysU4yAHXS+0G4+rQul2Tnli+ea/HvB+l8HVnoN9SEZyvXqxDVj7nDxUffzPKKJTzqdBXMZ5qsUwdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(accesstoken)


#chappie
#handler = WebhookHandler('63bd28fd3a4fdadaa9655de644902fcc')
#khun_sinmai
#handler = WebhookHandler('1271b23fb3f7217041dcaa37548f7bdd')
#rvp
channelsecret = 'f375e3fce9c1ac3548f0f40d4ef8238d'
handler = WebhookHandler(channelsecret)

bottestgroup = 'Cbe8afa803412d3558dffcc9a1a8c4a71'

# def shutdown_server():
#     func = request.environ.get('werkzeug.server.shutdown')
#     if func is None:
#         raise RuntimeError('Not running with the Werkzeug Server')
#     func()

@app.route("/getResponse")
def hello():
     return "Hello World!"
    
#methods=['POST']

@app.route("/webhook", methods=['GET', 'POST'])
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
    if request.method == 'POST':
        return 'OK',200


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    
    words = event.message.text
    if 'สวัสดี' in words:
        profile = line_bot_api.get_profile(event.source.user_id)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(
                    text='สวัสดีค่ะ, \n' + event.source.user_id
                )
            ]
        )
    elif 'ลงทะเบียน:' in words:
        profile = line_bot_api.get_profile(event.source.user_id)
        words = words.replace('ลงทะเบียน:','')
        words = words.replace(' ','')

        if len(words) == 6:

            params = {
                'EmpId': words,
                'UserId': event.source.user_id,
                'BotName': "@rvpinsurance",
                'ChannelSecret': channelsecret,
                'AccessToken': accesstoken,
            }


            api_key = 'UlZQLklULklUNC4wLjEyMzQ1Iw=='

            dataResponse = requests.post(url+'LINEManagement/CL_LINERegister?api_key='+api_key, params)
            dataResponse = dataResponse.json()
            print(dataResponse)
            MessageResponse = 'ไม่สามารถทำรายการได้'

            dataResponse_Status = dataResponse.get('Status')
            print(dataResponse_Status)
            if dataResponse_Status == 1:
                dataResponse_Data = dataResponse.get('Data')
                data_registerstatus = dataResponse_Data['RegisterStatus']
                print(data_registerstatus)

                if data_registerstatus ==  '1':
                    MessageResponse = 'การสมัครของคุณ '+ profile.display_name+' \nรหัสพนักงาน '+words +'\nการลงทะเบียนเสร็จสมบูรณ์'       
                elif data_registerstatus == '-1':
                    MessageResponse = 'การสมัครของคุณ '+ profile.display_name+' \nมีการลงทะเบียนด้วยไลน์ไอดีนี้ไปแล้ว \nการลงทะเบียนไม่สมบูรณ์'
                elif data_registerstatus == '-2':
                    MessageResponse = 'การสมัครของคุณ '+ profile.display_name+' \nรหัสพนักงาน '+words +'\nมีการลงทะเบียนด้วยรหัสพนักงานนี้ไปแล้ว \nการลงทะเบียนไม่สมบูรณ์'
                elif data_registerstatus == '-3':
                    MessageResponse = 'การสมัครของคุณ '+ profile.display_name+' \nไม่มีรหัสพนักงานนี้ในระบบ \nการลงทะเบียนไม่สมบูรณ์'

                try: 
                    line_bot_api.reply_message(
                        event.reply_token, [
                            TextSendMessage(
                                text=MessageResponse
                            )
                        ]
                    )
                except:
                    line_bot_api.push_message(bottestgroup,
                    TextSendMessage(text='กรุณาเพิ่มเพื่อนกับบอทไลน์'))
        else:
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(
                        text='รูปแบบการสมัครของคุณ '+ profile.display_name+' ไม่ถูกต้อง'
                    )
                ]
            )

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


if __name__ == "__main__":
    app.run()

