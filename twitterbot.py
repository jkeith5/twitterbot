import tweepy
import wikipedia
from datetime import datetime as dt
import time
import twitterkeys as tk
import requests
import random

#constructs the URL that is to be posted
def urlConstruction(topic):
    temp = topic.replace(' ','_')
    fin = "https://en.wikipedia.org/wiki/"+temp
    return fin

#post the tweet
def postTweet(auth, wiki, preface):
    api = tweepy.API(auth)
    api.update_status(preface+""+wiki)

def constructPreface(file):
    #load the prefaces into a list, then randomly chooses one to return
    prefaceList = []
    for line in file:
        prefaceList.append(line)
    print(random.choice(prefaceList))
    return random.choice(prefaceList)

#asks wiki API for a random article(specified by rnnamespace being 0
def wikiRandomCall():
    #connects to the API, requests and parses received JSON.
    S = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"
    PARAMS = {
        "action": "query",
        "rnnamespace":"0",
        "format": "json",
        "list": "random",
        "rnlimit": "1"
    }
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    RANDOMS = DATA["query"]["random"]
    for r in RANDOMS:
        if (r["id"]):
            titlestring = (r["title"])
    wikiURL = urlConstruction(titlestring)
    S.close()
    return wikiURL

prefaceFile = open("prefacesFile.txt", "r")
prefaceFinal = constructPreface(prefaceFile)
prefaceFile.close()


now= dt.now()
current_time = now.strftime("%H:%M:%S")
print("Current time = ", current_time)

consumer_key = tk.consumer_key
consumer_secret = tk.consumer_secret
access_token = tk.access_token
access_token_secret = tk.access_token_secret

    #auth to twitter
auth = tweepy.OAuthHandler(consumer_key,
            consumer_secret)
auth.set_access_token(access_token,
                      access_token_secret)

api = tweepy.API(auth)

try:
    redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
    print('Error! Failed to get request token.')

#get the random wiki page
wiki = wikiRandomCall()
postTweet(auth, wiki, prefaceFinal)
    

