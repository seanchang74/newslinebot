from django.conf import settings
import requests,datetime,time
from urllib.parse import urlencode
from newsapi import NewsApiClient

from linebot import LineBotApi
from newslinebot.models import comment
from linebot.models import TextSendMessage, StickerSendMessage, QuickReply, QuickReplyButton, TemplateSendMessage, URITemplateAction, CarouselTemplate, CarouselColumn, ButtonsTemplate, MessageAction
admin_uid = "U8795ae526cd325236226d2e4cda3197f"

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
# everything_url = 'https://newsapi.org/v2/everything'
# top_headline_url = 'https://newsapi.org/v2/top-headlines'
# API_KEY = '0d978f7c0a1a479f8fbabe4c4046d12d'
newsapi = NewsApiClient(api_key='0d978f7c0a1a479f8fbabe4c4046d12d')
# ImageURL = []
# title = []
# description = []
# URL = []

def sendJustSee(event):
    all_articles = newsapi.get_everything(domains='ettoday.net,setn.com,ltn.com.tw,udn.com,bbc.com,cw.com.tw',
                                          language='zh',
                                          from_param=datetime.date.today(),
                                          to=datetime.date.today(),
                                          sort_by='popularity')

    try:
        results =  all_articles['articles'][0]
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = '請求資料時發生錯誤，麻煩重試一次!'))
        return
    time.sleep(3)
    
    try:
        if(results['urlToImage'] == None):
                ImageURL = 'https://images.pexels.com/photos/3866816/pexels-photo-3866816.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940'
        else:
            ImageURL = results['urlToImage']
        message = TemplateSendMessage(
            alt_text = '按鈕樣板',
            template = ButtonsTemplate(
                thumbnail_image_url = ImageURL,
                title = results['title'],
                text = results['description'],
                actions = [
                    URITemplateAction(
                        label = '查看原文',
                        uri = results['url']
                    )
                ]
            )
        )
        
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = '發生錯誤'))

def sendTopic(event):
    try:
        message = TextSendMessage(text='請問你想看什麼主題呢?',
                                    quick_reply=QuickReply(
                                        items=[
                                            QuickReplyButton(
                                                action=MessageAction(label="商業",
                                                text="business")
                                            ),
                                            QuickReplyButton(
                                                action=MessageAction(label="娛樂",
                                                text="entertainment")
                                            ),
                                            QuickReplyButton(
                                                action=MessageAction(label="一般",
                                                text="general")
                                            ),
                                            QuickReplyButton(
                                                action=MessageAction(label="健康",
                                                text="health")
                                            ),
                                            QuickReplyButton(
                                                action=MessageAction(label="科學",
                                                text="science")
                                            ),
                                            QuickReplyButton(
                                                action=MessageAction(label="運動",
                                                text="sports")
                                            ),
                                            QuickReplyButton(
                                                action=MessageAction(label="科技",
                                                text="technology")
                                            ),
                                            QuickReplyButton(
                                                action=MessageAction(label="都來一點",
                                                text="everything")
                                            ),
                                        ]
                                    ))
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = '發生錯誤'))

def sendHeadline(event,mycategory):
    if(mycategory == 'everything'):
        top_headlines = newsapi.get_top_headlines(language='zh',
                                                  country='tw')
    else:
        top_headlines = newsapi.get_top_headlines(language='zh',
                                                  country='tw',
                                                  category=mycategory)

    try:
        results =  top_headlines['articles'][0]
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = '請求資料時發生錯誤，麻煩重試一次!'))
        return
    time.sleep(3)
    
    try:
        if(results['urlToImage'] == None):
                ImageURL = 'https://images.pexels.com/photos/3866816/pexels-photo-3866816.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940'
        else:
            ImageURL = results['urlToImage']
        message = TemplateSendMessage(
            alt_text = '按鈕樣板',
            template = ButtonsTemplate(
                thumbnail_image_url = ImageURL,
                title = results['title'],
                text = results['description'],
                actions = [
                    URITemplateAction(
                        label = '查看原文',
                        uri = results['url']
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = "發生錯誤!"))

def sendSearch(event,query):
    all_articles = newsapi.get_everything(q=query,
                                      from_param=datetime.date.today() - datetime.timedelta(days=3),
                                      to=datetime.date.today(),
                                      language='zh',
                                      sort_by='relevancy')

    try:
        results =  all_articles['articles'][0]

    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = '請求資料時發生錯誤，麻煩重試一次!'))
        return  
    time.sleep(3)
    
    try:
        if(results['urlToImage'] == None):
                ImageURL = 'https://images.pexels.com/photos/3866816/pexels-photo-3866816.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940'
        else:
            ImageURL = results['urlToImage']
        message = TemplateSendMessage(
            alt_text = '按鈕樣板',
            template = ButtonsTemplate(
                thumbnail_image_url = ImageURL,
                title = results['title'],
                text = results['description'],
                actions = [
                    URITemplateAction(
                        label = '查看原文',
                        uri = results['url']
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = '發生錯誤'))

def manageform(event,reply,LINEID):
    try:
        flist = reply[3:].split('/')
        cname = flist[0]
        cemail = flist[1]
        ccomment = flist[2]
        
        unit = comment.objects.create(cuid=LINEID, name=cname, email=cemail, comments=ccomment)
        unit.save()

        text1 = "姓名:" + cname
        text1 += "\n電子郵件:" + cemail
        text1 += "\n評論:" + ccomment
        
        message = [
            TextSendMessage(  
                    text = "以下是你輸入的資料"
                ),
            TextSendMessage(  
                    text = text1
                ),
            TextSendMessage(  
                    text = "感謝你的寶貴意見，我們會盡快通知客服處理"
                ),
            StickerSendMessage(
                package_id = '2',
                sticker_id = '41'
            )
        ]
        line_bot_api.reply_message(event.reply_token,message)

    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='資料處理發生錯誤！'))
