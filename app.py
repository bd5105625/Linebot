import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
# from linebot.models import MessageEvent, TextMessage, TextSendMessage , TemplateSendMessage, ButtonsTemplate, 
#                  PostbackAction, MessageAction, URIAction
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction , ImageSendMessage
from fsm import TocMachine
from utils import send_text_message , set_button , send_image
# from ptt import *

load_dotenv()

buttons_template = TemplateSendMessage(
    alt_text='Buttons Template',
    template=ButtonsTemplate(
        title='批踢踢熱門搜尋',
        text='選擇全站或是特定看板熱門文章',
        thumbnail_image_url='https://photo.sofun.tw/2016/02/PTT-Overload-Port-Logo.jpg',
        actions=[
            MessageTemplateAction(
                label='熱門文章',
                text='熱門文章'
            ),
            MessageTemplateAction(
                label='熱門新聞',
                # text='go to state2',
                text='熱門新聞',
            ),
            MessageTemplateAction(
                label='看板功能',
                # text='go to state2',
                text='看板功能',
            ),
            MessageTemplateAction(
                label='最新文章',
                # text='go to state2',
                text='最新文章',
            ),
        ]   
        )
)

button_intoboard = TemplateSendMessage(
    alt_text='Buttons Template',
    template=ButtonsTemplate(
        title='看板內容',
        text='選擇特定看板何種內容，點選完輸入看板名稱',
        thumbnail_image_url='https://photo.sofun.tw/2016/02/PTT-Overload-Port-Logo.jpg',
        actions=[
            MessageTemplateAction(
                label='看板最新文章',
                text='看板最新文章'
            ),
            MessageTemplateAction(
                label='看板熱門文章',
                text='看板熱門文章',
            ),
        ]   
        )
)

picture = ImageSendMessage(
    original_content_url =  "https://imgur.com/aq9WZJy.jpg",
    preview_image_url = "https://i.imgur.com/aq9WZJy.jpg"
)

machine = TocMachine(
    states=["user", "state1", "state2" , "state3" , "state4" , "state5" , "state6"],  #熱門文章、熱門新聞、選擇看板、最新文章
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state1",
            "conditions": ["is_going_to_state1"],
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state2",
            "conditions": "is_going_to_state2",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state3",
            "conditions": "is_going_to_state3",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state4",
            "conditions": "is_going_to_state4",
        },
        {
            "trigger": "advance",
            "source": "state3",
            "dest": "state5",
            "conditions": "is_going_to_state5",
        },
        {
            "trigger": "advance",
            "source": "state3",
            "dest": "state6",
            "conditions": "is_going_to_state6",
        },
        {
            "trigger": "go_back", 
            "source": ["state1", "state2" , "state3" , "state4" , "state5" , "state6"], 
            "dest": "user", 
        },
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)



    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        if event.message.text.lower() == "draw":    #傳送FSM圖片
            # strr = "Here"
            send_image(event.reply_token , picture)  
            print("Here in image send")  
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        # if machine.state == "state1":       #取得熱門
        #     machine.gethot(event , event.message.text)
        # elif machine.state == "state2":     #取得新聞
        #     machine.getnews(event , event.message.text)
        if event.message.text.lower() == "button":
            try:
                set_button(event.reply_token , buttons_template)
            except LineBotApiError as e:
                # error handle
                raise e

        if machine.state == "state5":     #特定看板最新文章
            board = event.message.text
            machine.getboardnew(event , board) 
        elif machine.state == "state6":     #特定看板熱門文章
            board = event.message.text
            machine.getboard(event , board) 
        # elif machine.state == "state3":
        #     try:
        #         set_button(event.reply_token , button_intoboard)
        #     except LineBotApiError as e:
        #         # error handle
        #         raise e
        #     response = machine.advance(event , event.message.text)
        #     if response == False:
        #         send_text_message(event.reply_token, "請透過選單選取或是傳送Button呼叫選單")
        else:
            response = machine.advance(event , event.message.text)
            if response == False:
                send_text_message(event.reply_token, "請透過選單選取或是傳送Button呼叫選單")
        if machine.state == "state3":
            try:
                set_button(event.reply_token , button_intoboard)
            except LineBotApiError as e:
                # error handle
                raise e
            response = machine.advance(event , event.message.text)
            if response == False:
                send_text_message(event.reply_token, "請透過選單選取或是傳送Button呼叫選單")


 
        if machine.state == "state1":       #取得熱門
            machine.gethot(event)
        elif machine.state == "state2":     #取得新聞
            machine.getnews(event) 
        elif machine.state == "state4":     #取得文章
            machine.getarticle(event) 

            
        # if response == False:
        #     send_text_message(event.reply_token, "請透過選單選取")
    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
