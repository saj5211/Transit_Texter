import smtplib
import time
import imaplib
import email
from twilio.rest import Client
import schedule
import threading

ORG_EMAIL = "@gmail.com"
FROM_EMAIL = "emailtestpython5211"+ORG_EMAIL
FROM_PWD = "pythonemail212"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993
account_sid = "AC8506e95acd53cd7ea689a3b50e5a96b3"
auth_token = "78c3fe220d0b712093f99165983ecb21"
client  = Client(account_sid,auth_token)


def readmail():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL, FROM_PWD)
        mail.select('inbox')
        type, data = mail.search(None, 'UNSEEN')
        mail_ids = data[0]
        id_list = mail_ids.split()
        last_email_id = int(id_list[-1])
        type, data = mail.fetch(last_email_id, "(RFC822)")

        for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    email_subject = msg['subject']
                    email_from = msg['from']
                    if msg.is_multipart():
                        for part in msg.walk():
                            ctype = part.get_content_type()
                            cdispo = str(part.get('Content-Disposition'))
                            if ctype == 'text/plain' and 'attachment' not in cdispo:
                                body = part.get_payload(decode=True)  # decode
                                break
                    else:
                        body = msg.get_payload(decode=True)

                    if (email_from == "Next Ride <NextRide@brampton.ca>"):
                        client.messages.create(
                            to="+14164545756",
                            from_="+16478007048",
                            body=body
                        )


    except:
        print"error"
def repeat():
    i=0
    while i<=5:
        readmail()
        #time.sleep(1)
        i+=1
    exit()
repeat()
