import os

from linebot import LineBotApi, WebhookParser
from linebot.models import TextSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction , ImageSendMessage


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def set_button(reply_token , button):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token , button)

    return "OK"

def send_image(reply_token , image):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token , image)

    return "OK"
"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
