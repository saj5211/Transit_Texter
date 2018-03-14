
import logging
import os

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from BeautifulSoup import BeautifulSoup
import UserDB
from Transit_Lookup import look_up


# [START configuration]
TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_NUMBER = os.environ['TWILIO_NUMBER']
# [END configuration]


app = Flask(__name__)



# [START receive_sms]
@app.route('/sms/receive', methods=['POST'])
def receive_sms():
	"""Receives an SMS message and replies with a simple greeting."""
	number = request.values.get('From')
	response = request.values.get('Body')
	resp = MessagingResponse()
	number = number[1:]
	greeting = UserDB.check_user(number)
    try:
        if "set-default-to" in response:
            response = response.split(" ")
            result = UserDB.changePref(number, "default", response[1])
        elif (("ttc" in response) or ("bram" in response)):
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
    except:
        result = "Please Try Again"
    resp.message(result)
	return str(resp)

# [END receive_sms]


if __name__ == '__main__':
	# This is used when running locally. Gunicorn is used to run the
	# application on Google App Engine. See entrypoint in app.yaml.
	app.run(host='127.0.0.1', port=8080, debug=True)
# [END app]
