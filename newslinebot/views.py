from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
from newslinebot.models import users, comment
from module import func


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
category = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology', 'everything']

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        for event in events:
            if isinstance(event, MessageEvent):
                userid = event.source.user_id
                if not users.objects.filter(uid=userid).exists():
                    unit = users.objects.create(uid=userid, state='normal')
                    unit.save()
                    mode = 'normal'
                else:
                    unit = users.objects.get(uid=userid)
                    mode = unit.state

                mtext = event.message.text

                if mtext[:3] == '###' and len(mtext) > 3:
                    if not comment.objects.filter(cuid=userid).exists():
                        func.manageform(event,mtext,userid)
                    else:
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='你已經填寫過表單了，客服將馬上處理你的問題!'))
                elif mtext == '@隨便看看':
                    func.sendJustSee(event)
                elif mtext == '@今日頭條':
                    func.sendTopic(event)
                elif mtext == '@關鍵字搜索' and mode == 'normal':
                    unit = users.objects.get(uid=userid)
                    unit.state = 'search'
                    unit.save()
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text = '請問你想要搜尋什麼呢?\n可以直接用下方鍵盤輸入哦!'))
                elif mode == 'search':
                    unit = users.objects.get(uid=userid)
                    unit.state = 'normal'
                    unit.save()
                    func.sendSearch(event,mtext)
                elif mtext in category:
                    func.sendHeadline(event,mtext)
                                   
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


