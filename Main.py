import json
import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import UserDB
from Transit_Lookup import look_up
import Subscriptions
from UserDB import checkPref
import streaming_methods
import sys, os
from flask_assistant import Assistant, ask, tell


# [START configuration]
#TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
#TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
#TWILIO_NUMBER = os.environ['TWILIO_NUMBER']
## [END configuration]


app = Flask(__name__)



# Twillio Setup
@app.route('/sms/receive', methods=['POST'])
def receive_sms():
    """Receives an SMS message and replies with a simple greeting."""
    number = request.values.get('From')
    response = request.values.get('Body')
    resp = MessagingResponse()
    number = number[1:]
    greeting = UserDB.check_user(number)
    result = responseAnalyze(response, number, greeting)
    resp.message(result)
    return str(resp)

#MESSENGER SETUP
PAT = 'EAAFXbZA27CG8BAL57UMqSBigg7O08ms8FgCCYd1jVbtx0AZCnrFjkongGyi3XEuaZCvLrH0r3ZCIIakMxqOmbNIDS8ZA8Cw8mqiAl7FVm8IoY323RyyvLZB7akac7mVK5g73Lc8BP2Ex0D6LlDb993JtjrYdZA9xcp8Ehf1dUQXvAZDZD'

@app.route('/mess', methods=['GET'])
def handle_verification():
  print "Handling Verification."
  if request.args.get('hub.verify_token', '') == 'my_voice_is_my_password_verify_me':
    print "Verification successful!"
    return request.args.get('hub.challenge', '')
  else:
    print "Verification failed!"
    return 'Error, wrong validation token'

@app.route('/mess', methods=['POST'])
def handle_messages():
  print "Handling Messages"
  payload = request.get_data()
  print payload
  for sender, message in messaging_events(payload):
    print "Incoming from %s: %s" % (sender, message)
    send_message(PAT, sender, message)
  return "ok"

def messaging_events(payload):
  """Generate tuples of (sender_id, message_text) from the
  provided payload.
  """
  data = json.loads(payload)
  messaging_events = data["entry"][0]["messaging"]
  print data
  for event in messaging_events:
    if "message" in event and "text" in event["message"]:
       response = event["message"]["text"].encode('unicode_escape')
       number = event["sender"]["id"]
       greeting = UserDB.check_user(number)
       result = responseAnalyze(response,number,greeting)
       yield event["sender"]["id"], result
    else:
      yield event["sender"]["id"], "I can't echo this"

#Google Assistant Setup
assist = Assistant(app, route='/assist')
@assist.action('greeting')
def greet_and_start():
    speech = "Hey! Welcome to Transit Texter"
    return ask(speech)

@assist.action("bus_number", mapping={'stop_number':'sys.number', 'bus_agency':'agency','bus_number':'sys.number',
                                      'setting': 'setting', 'list': 'list'})
def ask_stop(stop_number,bus_agency,bus_number,setting,list):
    if stop_number and bus_agency and list:
        response = bus_agency + " " + stop_number + " list"
    elif stop_number and bus_number and bus_agency:
        response = bus_agency + " " + stop_number + " " + bus_number
    elif stop_number and bus_agency:
        response = bus_agency + " " + stop_number
    elif stop_number and bus_number:
        response = stop_number + " " + bus_number
    elif stop_number:
        response = stop_number
    else:
        return ask("Please Try Again")
    result = responseAnalyze(response, "1", UserDB.check_user("1"))

    return ask(result)



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
agencies = ["bram", "ttc","yrt"]



def responseAnalyze(response, number, greeting):
    print response
    try:
        response = response.lower()
        if "help" in response:
            result = "Welcome to Transit Texter \nby: Saj \n\nQuickstart Guide " \
                     "\n-get next bus time --> [stop#] \n-get specific bus time --> [stop#] [bus#] " \
                     "\n-get list of all buses --> [stop#] list " \
                     "\n-get bus time from another transit agency add [agency name] to the front" \
                     "\n\nSupported cities" \
                     "\n-Brampton Transit [bram]" \
                     "\n-TTC [ttc]"\
                     "\n-York Regional Transit [yrt]" \
                     "\n\nYour default setting is set to bram" \
                     "\n-to change setting --> default [agency name] " \
                     "\n\nSubscriptions (!Optional)" \
                     "\n-turn on subscriptions --> open subscription" \
                     "\n-turn off subscriptions --> close subscription" \
                     "\n-check subscriptions --> check subscription" \
                     "\n-add stop to subscriptions --> add ![agency] [stop#] [time]" \
                     "\n-remove stop from subscriptions --> remove [stop#]" \
                     "\n-reset subscriptions --> subscription reset" \
                     "\n\nIntroducing Streaming (!Optional)" \
                     "\nGet notifications every 30secs for any stop" \
                     "\n-add stop to stream --> stream [stop#] ![bus#] ![agency]" \
                     "\n-stop stream --> stop stream"\
                     "\n\n Type 'Help' for Help!"
        elif "default" in response:
            response = response.split(" ")
            if len(response) == 1:
                result = "Default: " + checkPref(number)
            else:
                result = UserDB.changePref(number, "default", response[1])
        elif "stop stream" in response:
            result = streaming_methods.stream_stop(number)
        elif "stream" in response:
            if len(response.split(" ")) == 2:
                response = response.split(" ")
                result = streaming_methods.add_stream(number, response[1], False, False)
            elif any(x in response for x in agencies):
                response = response.split(" ")
                result = streaming_methods.add_stream(number, response[1], response[2], response[3])
            else:
                response = response.split(" ")
                result = streaming_methods.add_stream(number, response[1], response[2],False)
        elif "close subscription" in response:
            result = Subscriptions.changeSubPref(number, "inactive")
        elif "open subscription" in response:
            result = Subscriptions.changeSubPref(number, "active")
        elif "subscription reset" in response:
            result = Subscriptions.resetSub(number)
        elif "check subscription" in response:
            result = Subscriptions.subscriptionCheck(number)
        elif "add" in response:
            response = response.split(" ")
            if len(response) == 4 :
                result = Subscriptions.update(number, response[1],response[2], response[3])
            else:
                result = Subscriptions.update(number, False, response[1],response[2])
        elif "remove" in response:
            response = response.split(" ")
            if len(response)==3:
                result = Subscriptions.remove(number, response[1],response[2])
            else:
                result = Subscriptions.remove(number, False, response[1])
        elif any(x in response for x in agencies):
            response = response.split(" ")
            if (len(response) == 3):
                result = look_up(response[1], response[2], response[0])
            else:
                result = look_up(response[1], False, response[0])
        elif (" " in response):
            response = response.split(" ")
            result = look_up(response[0], response[1], UserDB.checkPref(number))
        else:
            result = look_up(response, False, str(UserDB.checkPref(number)))
        if "user" not in greeting:
            result = greeting + "\n\n\n" + str(result)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        result = "Please Try Again"
    return result

# [END receive_sms]

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8888, threaded=True)
# [END app]
