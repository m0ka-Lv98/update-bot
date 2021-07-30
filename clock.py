from main import USER_ID
from linebot import (
   LineBotApi, WebhookHandler
)
from linebot.exceptions import (
   InvalidSignatureError
)
from linebot.models import (
   FollowEvent, MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction
)
from twitter import gettwitterdata
from apscheduler.schedulers.blocking import BlockingScheduler
import yaml
import os
#環境変数からLINE Access Tokenを設定
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
#環境変数からLINE Channel Secretを設定
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
with open('api_keys.yaml', 'r') as f:
   config = yaml.safe_load(f)
GROUP_ID = config['line']['GROUP_ID']
USER_ID = config['line']['USER_ID']
ID = GROUP_ID
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
sched = BlockingScheduler(timezone='Asia/Tokyo')

@sched.scheduled_job('cron', hour=20, minute=0)
def job_function():
   tweet = gettwitterdata(sched=True)
   if len(tweet):
       tweet = 'アップデート情報が更新されました！\n\n' + tweet
       line_bot_api.push_message(
           ID,
           TextSendMessage(text=tweet))

if __name__ == "__main__":
    sched.start()