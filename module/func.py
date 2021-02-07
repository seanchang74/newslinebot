from django.conf import settings
import requests,datetime,time
from urllib.parse import urlencode

from linebot import LineBotApi
from newslinebot.models import comment
from linebot.models import TextSendMessage, StickerSendMessage, QuickReply, QuickReplyButton, TemplateSendMessage, URITemplateAction, CarouselTemplate, CarouselColumn, ButtonsTemplate, MessageAction
admin_uid = "U8795ae526cd325236226d2e4cda3197f"

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
everything_url = 'https://newsapi.org/v2/everything'
top_headline_url = 'https://newsapi.org/v2/top-headlines'
API_KEY = '0d978f7c0a1a479f8fbabe4c4046d12d'

ImageURL = []
title = []
description = []
URL = []

def sendJustSee(event,LINEID):
    params = {
        "from" : datetime.date.today(),
        "to" : datetime.date.today(),
        "domains" : {"ettoday.net","setn.com","ltn.com.tw","udn.com","bbc.com","cw.com.tw"},
        "language" : "zh",
        "sortBy" : "popularity",
        "apiKey" : API_KEY
    }
    params_encoded = urlencode(params)
    request_url = f"{everything_url}?{params_encoded}"
    request_url = request_url.replace('%27%2C+%27',',').replace('%7B%27','').replace('%27%7D','')
    try:
        r = requests.get(request_url)
        results =  r.json()['articles']
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = '請求資料時發生錯誤，麻煩重試一次!'))
        return

    if(len(ImageURL) != 0 or len(title) != 0 or len(description) != 0 or len(URL) != 0):
        ImageURL.clear()
        title.clear()
        description.clear()
        URL.clear()
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text = '擷取新聞資料中...'))
    time.sleep(3)
    try:
        for result in results:
            if(result['urlToImage'] == None):
                ImageURL.append('https://images.pexels.com/photos/3866816/pexels-photo-3866816.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940')
            else:
                ImageURL.append(result['urlToImage'])
            title.append(result['title'])
            description.append(result['description'])
            URL.append(result['url'])
            break
    except:
        pass
    
    try:
        message = TemplateSendMessage(
            alt_text = '按鈕樣板',
            template = ButtonsTemplate(
                thumbnail_image_url = str(ImageURL[0]),
                title = title[0],
                text = description[0],
                actions = [
                    URITemplateAction(
                        label = '查看原文',
                        uri = str(URL[0])
                    )
                ]
            )
        )
        
        # message = TemplateSendMessage(  #Carousel 要給實際的數值
        #     alt_text='Carousel template',
        #     template=CarouselTemplate(
        #         columns=[
        #             CarouselColumn(
        #                 thumbnail_image_url='https://i.imgur.com/uGBPO9l.png',
        #                 title='this is menu1',
        #                 text='this is menu1',
        #                 actions=[
        #                     URITemplateAction(
        #                         label = '查看原文',
        #                         uri = 'https://i.imgur.com/uGBPO9l.png'
        #                     )
        #                 ]
        #             ),
        #             CarouselColumn(
        #                 thumbnail_image_url='https://i.imgur.com/uGBPO9l.png',
        #                 title='this is menu1',
        #                 text='this is menu1',
        #                 actions=[
        #                     URITemplateAction(
        #                         label = '查看原文',
        #                         uri = 'https://i.imgur.com/uGBPO9l.png'
        #                     )
        #                 ]
        #             )
        #         ]
        #     )
        # )
        line_bot_api.push_message(to=LINEID,messages=[message])
    except:
        line_bot_api.push_message(to=LINEID,messages=[TextSendMessage(text = '發生錯誤!')])

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

def sendHeadline(event,category,LINEID):
    if(category == 'everything'):
        params = {
            "country" : "tw",
            "apiKey" : API_KEY
        }
    else:
        params = {
            "country" : "tw",
            "category" : category,
            "apiKey" : API_KEY
        }
    params_encoded = urlencode(params)
    request_url = f"{top_headline_url}?{params_encoded}"

    if(len(ImageURL) != 0 or len(title) != 0 or len(description) != 0 or len(URL) != 0):
        ImageURL.clear()
        title.clear()
        description.clear()
        URL.clear()

    try:
        r = requests.get(request_url)
        results =  r.json()['articles']
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = '請求資料時發生錯誤，麻煩重試一次!'))
        return

    line_bot_api.reply_message(event.reply_token,TextSendMessage(text = '擷取新聞資料中...'))
    time.sleep(3)
    try:
        for result in results:
            if(result['urlToImage'] == None):
                ImageURL.append('https://images.pexels.com/photos/3866816/pexels-photo-3866816.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940')
            else:
                ImageURL.append(result['urlToImage'])
            title.append(result['title'])
            description.append(result['description'])
            URL.append(result['url'])
            break
    except:
        pass
    
    try:
        message = TemplateSendMessage(
            alt_text = '按鈕樣板',
            template = ButtonsTemplate(
                thumbnail_image_url = str(ImageURL[0]),
                title = title[0],
                text = description[0],
                actions = [
                    URITemplateAction(
                        label = '查看原文',
                        uri = str(URL[0])
                    )
                ]
            )
        )
        # message = TextSendMessage(text = (ImageURL[0] + '\n' + title[0] + '\n' + description[0] + '\n' + URL[0]))
        line_bot_api.push_message(to=LINEID,messages=[message])
    except:
        line_bot_api.push_message(to=LINEID,messages=[TextSendMessage(text = '發生錯誤!')])

def sendSearch(event,query,LINEID):
    params = {
        "q" : query,
        "language" : "zh",
        "sortBy" : "relevancy",
        "from" : datetime.date.today() - datetime.timedelta(days=3),
        "to" : datetime.date.today(),
        "apiKey" : API_KEY
    }
    params_encoded = urlencode(params)
    request_url = f"{everything_url}?{params_encoded}"

    if(len(ImageURL) != 0 or len(title) != 0 or len(description) != 0 or len(URL) != 0):
        ImageURL.clear()
        title.clear()
        description.clear()
        URL.clear()

    try:
        r = requests.get(request_url)
        results =  r.json()['articles']
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = '請求資料時發生錯誤，麻煩重試一次!'))
        return
        
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text = '擷取新聞資料中...'))
    time.sleep(3)
    try:
        for result in results:
            if(result['urlToImage'] == None):
                ImageURL.append('https://images.pexels.com/photos/3866816/pexels-photo-3866816.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940')
            else:
                ImageURL.append(result['urlToImage'])
            title.append(result['title'])
            description.append(result['description'])
            URL.append(result['url'])
            break
    except:
        pass
    
    try:
        message = TemplateSendMessage(
            alt_text = '按鈕樣板',
            template = ButtonsTemplate(
                thumbnail_image_url = str(ImageURL[0]),
                title = title[0],
                text = description[0],
                actions = [
                    URITemplateAction(
                        label = '查看原文',
                        uri = str(URL[0])
                    )
                ]
            )
        )
        # message = TextSendMessage(text = (ImageURL[0] + '\n' + title[0] + '\n' + description[0] + '\n' + URL[0]))
        line_bot_api.push_message(to=LINEID,messages=[message])
    except:
        line_bot_api.push_message(to=LINEID,messages=[TextSendMessage(text = '發生錯誤!')])

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
