from Subscriptions import lookAndSend, sub_Check
import datetime

def InitTime():
    count2 = 0
    users = []
    agency = []
    stop = []
    time = {}
    diffs = []
    subs = sub_Check()
    for i in subs:
        data = i.split(",")
        users.append(data[0])
        stop.append(data[1])
        agency.append(data[2])
        time[subs.index(i)] = data[3]
    sorted_time = sorted((value, key) for (key, value) in time.items())
    class subscription:
        count2
        users
        agency
        stop
        sorted_time
    s = subscription()
    s.count2 = count2
    s.users = users
    s.agency = agency
    s.stop = stop
    s.sorted_time = sorted_time
    return s
def Time(count2,users, agency,stop,sorted_time):
    print "Subs Start"
    if count2 == 15:
        users = []
        agency = []
        stop = []
        time = {}
        diffs = []
        subs = sub_Check()
        for i in subs:
            data = i.split(",")
            users.append(data[0])
            stop.append(data[1])
            agency.append(data[2])
            time[subs.index(i)] = data[3]
        sorted_time = sorted((value,key) for (key,value) in time.items())
        count2 =0
    now = datetime.datetime.now()
    current = now.hour*60 + now.minute
    count2 += 1
    for i in sorted_time:
        count = 0
        state = False
        for j in i:
            if count == 0:
                if (current == int(j)):
                    state = True
            elif(count==1 and state == True):
                print "Sub Sent"
                lookAndSend([users[j], stop[j], agency[j]])

            count += 1
    print "Subs Finished " + str(count2) + " " + str(current)
