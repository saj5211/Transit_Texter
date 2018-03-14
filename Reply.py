from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import UserDB
from Transit_Lookup import look_up


app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""
    number = request.values.get('From',None)
    resp = MessagingResponse()
    response = request.form['Body']
    isUser = UserDB.check_user(number)
    number = number[1:]
    if "default" in response:
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
    if isUser:
        result = result
    else:
        result = str(UserDB.check_user(number)) + "\n\n\n" + str(result)

    resp.message(result)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
