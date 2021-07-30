import tweepy
import datetime
import yaml

LIMIT = 0

def gettwitterdata(account_list = ["Rainbow6Game", "Respawn"], sched=False, from_command=False):
    dt_now = datetime.datetime.utcnow()

    #Twitter APIを使用するためのConsumerキー、アクセストークン設定
    with open('api_keys.yaml', 'r') as f:
        config = yaml.safe_load(f)
    Consumer_key = config['twitter']['Consumer_key']
    Consumer_secret = config['twitter']['Consumer_secret']
    Access_token = config['twitter']['Access_token']
    Access_secret = config['twitter']['Access_secret']

    #認証
    auth = tweepy.OAuthHandler(Consumer_key, Consumer_secret)
    auth.set_access_token(Access_token, Access_secret)

    api = tweepy.API(auth, wait_on_rate_limit = True)
    tweet_list = []
    for Account in account_list:
        tweets = api.user_timeline(Account, count=100, page=1, exclude_replies=True, tweet_mode="extended")
        for tweet in tweets:
            if Account == "Rainbow6Game": flag = any(x in tweet.full_text.lower() for x in ['maintenance'])
            if Account == "Respawn": 
                flag = any(x in tweet.full_text.lower() for x in ['update']) and \
                       any(x in tweet.full_text.lower() for x in ['apex', 'legends', 'legend']) and \
                       not any(x in tweet.full_text.lower() for x in ['mobile'])
            if flag:
                print('date : ', tweet.created_at)      # 呟いた日時
                if sched and (dt_now - tweet.created_at).days > LIMIT:
                    continue
                
                tweet_list.append(tweet.created_at.strftime('%Y/%m/%d') + ' ' + tweet.user.name + '\n' + tweet.full_text)
                if from_command:
                    break
    output = f'\n{"="*20}\n'.join(tweet_list)
    print(output)
    return output

if __name__ == '__main__':
    gettwitterdata()