from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)

app = Flask(__name__)

line_bot_api = LineBotApi('63bd28fd3a4fdadaa9655de644902fcc')
handler = WebhookHandler('Py16F9GZePWwoBlq/r7aev30s9SUMYPsP9YAQpr4XBE2skelccadOvgDO8D04HMdNgmrVpu/N0edN8uBHVR36XlErDXbRFW2ODlr2yppKwSbKbhTTIPWe0sek7pzlvwySvDx04TSiPTTJDQAMrYjjgdB04t89/1O/w1cDnyilFU=')

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/webhook", methods=['GET','POST'])
def webhook():
    # get X-Line-Signature header value
   # signature = request.headers['X-Line-Signature']

    # get request body as text
   # body = request.get_data(as_text=True)
   # app.logger.info("Request body: " + body)

    # handle webhook body
  #  try:
  #      handler.handle(body, signature)
   # except InvalidSignatureError:
   #     abort(400)
    # if request.method == 'POST':
    return 'OK'
    

# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()