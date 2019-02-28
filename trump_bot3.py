import json
import requests
import time
import urllib
import random
import datetime
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import mysql.connector
from urllib3.exceptions import ProtocolError

TOKEN = ""
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""


def mysql_query_get_ids():

    mydb = mysql.connector.connect(
      host="localhost",
      user="",
      passwd="",
      database=""
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT chat_id FROM chat_id")
    myresult = mycursor.fetchall()
    #print (myresult)
    #mydb.commit()
    #print("< {}".format(temp_c))
    #mycursor.close()
    mydb.close()
    return myresult

def mysql_query_remove(chat_id):
    if str(chat_id) in str(a):
        #print("New chat_id added = {}".format(chat_id))

        mydb = mysql.connector.connect(
          host="localhost",
          user="",
          passwd="",
          database="trump_bot"
        )

        mycursor = mydb.cursor()
        mycursor.execute("DELETE FROM chat_id where chat_id = "+ str(chat_id))
        mydb.commit()
        #print("< {}".format(temp_c))
        mycursor.close()
        mydb.close()
        print("chatID : {} removed from DB".format(chat_id))


def mysql_query_insert(chat_id):
    #print("query")
    if str(chat_id) not in str(a):
        for x in a:
            print(x)
        #print("New chat_id added = {}".format(chat_id))
        mydb = mysql.connector.connect(
          host="localhost",
          user="",
          passwd="",
          database=""
        )

        mycursor = mydb.cursor()
        mycursor.execute("INSERT INTO chat_id (chat_id) VALUES (" + str(chat_id) +")")
        print("Subscription {} added".format(chat_id))
        mydb.commit()
        #print("< {}".format(temp_c))
        mycursor.close()
        mydb.close()
        a.append(chat_id)
        #for h in a:
            #print(h)
 

    else:
        #print("Already exists")
    
        pass


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    #print("content")
    return content


def get_json_from_url(url):
    #print("json_from_url")
    content = get_url(url)
    js = json.loads(content)
    #print(js)
    return js


def get_updates(offset=None):
    #print("getting tg updates")
    url = URL + "getUpdates?timeout=0"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    #print("updates received from TG")
    #print(js["message"]["text"])
    #if js["message"]["text"] == "/trump_sub":
     #   mysql_query_insert(js["message"]["chat"]["id"])
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def send_message(text, chat_id):
    #text = urllib.parse.quote_plus(text)
    
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)
    print("Tweet sent successfully")
    #return True


class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_status(self, status):
       # print("on_status")
        updates = get_updates()
        for update in updates["result"]:
            #if update["message"]["text"] == "/trump_sub":
                #print (update["message"]["chat"]["id"])
            mysql_query_insert(update["message"]["chat"]["id"])
        if status.author.id_str in ['25073877','1081336365684572160']:
            print("Tweet received")
            if updates["result"]:
                if len(updates["result"]) > 0:
                    update_ids = []
                    for update in updates["result"]:
                        if str(update["message"]["chat"]["id"]) in str(a):
                            update_ids.append(int(update["update_id"]))
                            last_update_id = max(update_ids) + 1
                            #message_array = update["message"]["text"].split(" ")
                            status = status.text
                            update["message"]["text"] = status
                            update["message"]["text"] = str(status)
                            text = update["message"]["text"]
                            #chat = update["message"]["chat"]["id"]
                            print('Sending tweet to {}'.format(a))
                            for i in a:
                                #print (i)
                                send_message(text, i)
                            #print("ei toimi")
                            return True


    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    a = []
    i = mysql_query_get_ids()
    for y in i:
        a.append(y[0])
    #print(a)
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    #for x in i:
        #print(x[0])
    #print("Existing chat_ids = " + i)


    while True:
        try:
            print("Initialize")
            stream.filter(follow=['25073877','1081336365684572160'])
        except(ProtocolError, AttributeError):
            print(ProtocolError, AttributeError)
            continue
