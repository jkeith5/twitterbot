import tweepy
import wikipedia
from datetime import datetime as dt
import schedule
import time
import twitterkeys as tk
import requests

execTime = "21:43"
listOfPages = []

S = requests.Session()
URL = "https://en.wikipedia.org/w/api.php"
PARAMS = {
    "action": "query",
    "rnnamespace":"0",
    "format": "json",
    "list": "random",
    "rnlimit": "1"
}

def urlConstruction(topic):
    temp = topic.replace(' ','_')
    fin = "https://en.wikipedia.org/wiki/"+temp
    return fin

def wikiRandomCall():
    

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    RANDOMS = DATA["query"]["random"]
    for r in RANDOMS:
        if (r["id"]):
            titlestring = (r["title"])
        print(titlestring)
    wikiURL = urlConstruction(titlestring)
    print(wikiURL)
    
    S.close()

    return wikiURL
    

wikiRandomCall()

def job():
    print ("I'm working...")
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


    #below posts a tweet
    api = tweepy.API(auth)
    api.update_status("Here's a random wikipedia article: " + wiki)
    return

schedule.every().day.at(execTime).do(job)

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute

    

