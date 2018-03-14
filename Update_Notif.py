import imaplib
from twilio.rest import Client
account_sid = "AC8506e95acd53cd7ea689a3b50e5a96b3"
auth_token = "78c3fe220d0b712093f99165983ecb21"
client  = Client(account_sid,auth_token)
numbers = ["+14164545756","+16474072884","+16474477201"]
body = "UPDATE 1.0.0\n\nTransit Texter is Officially Launched\n\nNew Features: \n-Added TTC\n-Migrated to GCloud\n-Added Preferences"
for i in numbers:
    client.messages.create(
        to=i,
        from_="+16478007048",
        body=body
    )