
import json
import requests
from flask import Flask, request
from Transit_Lookup import look_up
from UserDB import checkPref
import datetime
import sys, os

import pyrebase
config = {
  "apiKey": "AIzaSyAIl_jsu1fZj0fx4x34YOzWhZJHwq37DhQ",
  "authDomain": "transit-texter.firebaseapp.com",
  "databaseURL": "https://transit-texter.firebaseio.com",
  "storageBucket": "transit-texter.appspot.com",
  "serviceAccount": "accountkey.json"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

app = Flask(__name__)
#MESSENGER SETUP
PAT = 'EAAFXbZA27CG8BAL57UMqSBigg7O08ms8FgCCYd1jVbtx0AZCnrFjkongGyi3XEuaZCvLrH0r3ZCIIakMxqOmbNIDS8ZA8Cw8mqiAl7FVm8IoY323RyyvLZB7akac7mVK5g73Lc8BP2Ex0D6LlDb993JtjrYdZA9xcp8Ehf1dUQXvAZDZD'
def send_message(token, recipient, text):
  """Send the message text to recipient with id recipient.
  """

  r = requests.post("https://graph.facebook.com/v2.6/me/messages",
    params={"access_token": token},
    data=json.dumps({
      "recipient": {"id": recipient},
      "message": {"text": text.decode('unicode_escape')}
    }),
    headers={'Content-type': 'application/json'})
  if r.status_code != requests.codes.ok:
    print r.text

def sub_Check():
    users = db.child("users").get()
    sub_Data = []
    for user in users.each():
        try:
            subscription = user.val()
            if subscription["Subscription"]["activity"] == "active":
                for i  in subscription["Subscription"]:
                    if (i != "activity"):
                        sub_Data.append(str(user.key() + "," + i + "," + subscription["Subscription"].get(i)))

            else:
                pass;
        except Exception as e:
            print e
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            db.child("users").child(user.key()).child("Subscription").child("activity").set("inactive")
    return sub_Data

def subscriptionCheck(number):
    result = ""
    subscription = db.child("users").child(number).child("Subscription").get()
    subStuff = subscription.val()
    for i in subscription.val():
            if i !="activity":
                result += i[5:].upper() + " Stop " + i[:4] + " @ "
                if (int(subStuff[i])>720):
                       result += str(datetime.timedelta(minutes=(int(subStuff[i])-720)))[:-3] + "PM"+"\n"
                else:
                       result += str(datetime.timedelta(minutes=int(subStuff[i])))[:-3]+ "AM"+ "\n"
    status = db.child("users").child(number).child("Subscription").child("activity").get()
    return "Subscription Detail\n" + "Status: " + status.val() + "\n" + result

def update(number, agency,stop, time):
    if agency == False:
        stop += "," + checkPref(number)
    else:
        stop += "," + agency
    if "12" in time:
        if "am" in time:
            state = True
        else:
            state = False
        time = time.split(":")
        time[1] = time[1][:-2]
        print time
        if state:
            time = (int(time[0]) + 12) * 60 + int(time[1])
        else:
            time = int(time[0]) * 60 + int(time[1])
    elif "pm" in time or "am" in time:
        if "pm" in time:
            state = True
        else:
            state = False
        time = time.split(":")
        time[1] = time[1][:-2]
        print time
        if state:
            time = (int(time[0])+12) * 60 + int(time[1])
        else:
            time = int(time[0]) * 60 + int(time[1])
    elif "now" in time:
        time = datetime.datetime.now()
        time = int(time.hour)*60+int(time.minute)
    else:
        time = time.split(":")
        time = int(time[0]) * 60 + int(time[1])
    db.child("users").child(number).child("Subscription").child(stop).set(str(time))
    sub_Check()
    return "Your Subscriptions are Updated"


def lookAndSend (data):
    result = "Subscription Alert!\n Stop# " + data[1] + "\n" + look_up(data[1], "list", data[2])
    send_message(PAT, data[0], result)

def changeSubPref (number, state):
    if state == "active":
        db.child("users").child(number).child("Subscription").child("activity").set("active")
    else:
        db.child("users").child(number).child("Subscription").child("activity").set("inactive")
    return "Subscription state: " + state

def remove (number, agency,stop):
    subscription = db.child("users").child(number).child("Subscription").get()
    if agency == False:
        stop += "," + checkPref(number)
    else:
        stop += "," + agency
    for i in subscription.val():
        if (i == stop):
            db.child("users").child(number).child("Subscription").child(i).remove()

    return "Stop " + stop + " removed from your Subscriptions\n\n" + subscriptionCheck(number)
def resetSub (number):
    subscription = db.child("users").child(number).child("Subscription").get()
    for i in subscription.val():
        if (i != "activity"):
            db.child("users").child(number).child("Subscription").child(i).remove()
    db.child("users").child(number).child("Subscription").child("activity").set("inactive")
    return "Subscriptions Reset. Status set to inactive."

