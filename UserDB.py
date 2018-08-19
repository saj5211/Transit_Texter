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
def check_user(number):
    users = db.child("users").get()
    isUser= False
    welcomeMessage = "Welcome to Transit Texter \nby: Saj \n\nQuickstart Guide " \
             "\n-get next bus time --> [stop#] \n-get specific bus time --> [stop#] [bus#] " \
             "\n-get list of all buses --> [stop#] list " \
             "\n-get bus time from another transit agency add [agency name] to the front" \
             "\n\nSupported cities" \
             "\n-Brampton Transit [bram]" \
             "\n-TTC [ttc]" \
             "\n\nYour default setting is set to bram" \
             "\n-to change setting --> default [agency name] " \
             "\n\nSubscriptions (!Optional)" \
             "\n-turn on subscriptions --> open subscription" \
             "\n-turn off subscriptions --> close subscription" \
             "\n-check subscriptions --> check subscription" \
             "\n-add stop to subscriptions --> add ![agency] [stop#] [time]" \
             "\n-remove stop from subscriptions --> remove [stop#]" \
             "\n-reset subscriptions --> subscription reset" \
             "\\nIntroducing Streaming (!Optional)" \
             "\nGet notifications every 30secs for any stop" \
             "\n-add stop to stream --> stream [stop#] ![bus#] ![agency]" \
             "\n-stop stream --> stop stream" \
             "\n\n Type 'Help' for Help!"
    for use in users.each():
        if str(number) == str(use.key()):
            isUser = True


    if isUser==False:
        db.child("users").child(number).child("default").set("bram")
        return welcomeMessage
    else:
        return "user"


def checkPref(number):
    return db.child("users").child(str(number)).child("default").get().val()


def changePref(number, setting, value):
    db.child("users").child(number).child(setting).set(value)
    return "setting changed to: " + value
