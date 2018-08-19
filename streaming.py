from streaming_methods import streamAndSend, stream_check
from time import sleep

def InitStream():
    users = []
    agency = []
    stop = []
    route = []
    streams = stream_check()
    for i in streams:
        data = i.split(",")
        users.append(data[0])
        stop.append(data[1])
        agency.append(data[2])
        route.append(data[3])
    if users:
        for i in users:
            print "Stream Sent"
            streamAndSend(data)
    print "Stream end"

