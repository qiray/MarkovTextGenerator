import tweepy
import secrets

def get_api(cfg):
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)

def tweet(text, favorite):
    # Fill in the values noted in previous step here
    cfg = secrets.cfg
    api = get_api(cfg)
    status = api.update_status(status=text)
    if favorite and status.id:
        status = api.create_favorite(status.id)
    print(status)
