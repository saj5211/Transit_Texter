import Transit_Lookup
from UserDB import checkPref
import pyrebase
import requests
import json
import sys, os
config = {
  "apiKey": "AIzaSyAIl_jsu1fZj0fx4x34YOzWhZJHwq37DhQ",
  "authDomain": "transit-texter.firebaseapp.com",
  "databaseURL": "https://transit-texter.firebaseio.com",
  "storageBucket": "transit-texter.appspot.com",
  "serviceAccount": "accountkey.json"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
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

def add_stream (user, stop, route, agency):
    if agency == False:
        stop += "," + checkPref(user)
        agency = checkPref(user)
    else:
        stop += "," + agency
    if route == False:
        route = "list"
    db.child("users").child(user).child("Stream").child(stop).set(route)
    db.child("users").child(user).child("Stream").child("activity").set("active")
    result =  "Now Streaming: " + stop[:4] + " " + route + "\n" + Transit_Lookup.look_up(stop,route,agency)
    if "Bus Not Available" in result:
        stream_stop(user)
        return "Stop Cannot Be Streamed Right Now"
    else:
        return result

def stream_stop(user):
    subscription = db.child("users").child(user).child("Stream").get()
    for i in subscription.val():
        if (i != "activity"):
            db.child("users").child(user).child("Stream").child(i).remove()
    db.child("users").child(user).child("Stream").child("activity").set("inactive")
    return "Streaming Stopped."

def stream_check():
    users = db.child("users").get()
    sub_Data = []
    for user in users.each():
        try:
            subscription = user.val()
            if subscription["Stream"]["activity"] == "active":
                for i in subscription["Stream"]:
                    if (i != "activity"):
                        sub_Data.append(str(user.key() + "," + i + "," + subscription["Stream"].get(i)))

            else:
                pass;
        except Exception as e:
            print e
            db.child("users").child(user.key()).child("Stream").child("activity").set("inactive")
    return sub_Data

def streamAndSend(data):
    result = Transit_Lookup.look_up(data[1], data[3], data[2])
    if "Due" in result:
        stream_stop(data[0])
    elif "Bus Not Available" in result:
        stream_stop(data[0])
    send_message(PAT, data[0], result)

