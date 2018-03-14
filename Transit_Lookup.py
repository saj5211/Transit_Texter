import mechanize
from BeautifulSoup import BeautifulSoup
import UserDB
def look_up(stop_number, bus_number, agency):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Firefox')]
    if "bram" in agency:
        br.open("http://nextride.brampton.ca/mob/SearchBy.aspx")
        br.select_form(nr=0)
        br.submit(name="ctl00$mainPanel$lbtnSearchByStop")

        br.select_form(nr=0)
        br.form['ctl00$mainPanel$searchbyStop$txtStop']=stop_number
        br.select_form(nr=0)
        br.submit(name="ctl00$mainPanel$btnGetRealtimeSchedule")
        response = br.reload()
        route_name = []
        route_time = []
        soup = BeautifulSoup(response.read())
        table = soup.find("table", border=1)
        result = False
        try:

            if (bus_number == False):
                for row in table.findAll('tr')[1:]:
                    col = row.findAll('td')
                    route_name.append(col[0].string)
                    route_time.append(col[1].string)

                return str(route_name[0]) + "\n" + str(route_time[0])
            elif (bus_number == "list"):
                str23 = ""
                for row in table.findAll('tr')[1:]:
                    col = row.findAll('td')
                    route_name.append((col[0].string + "\n" + col[1].string + "\n"))
                if (len(route_name) > 5):
                    length = 5
                else:
                    length = int(len(route_name))
                for stuff in range(0, length):
                    str23 += route_name[stuff]

                return str(str23) + "\n"
            else:
                for row in table.findAll('tr')[1:]:
                    col = row.findAll('td')
                    for route in col[0]:
                        test = filter(unicode.isdigit, route.string)
                        test = test[0:len(bus_number)]
                        if (bus_number == test):
                            route_name.append(col[0].string)
                            route_time.append(col[1].string)
                            result = str(route_name[0]) + "\n" + str(route_time[0])
                            break
                if (result):
                    return result
                else:
                    return ("Bus Not Available")

        except:
            return "Please Try Again"

    elif "ttc" in agency:

        try:
            if bus_number=="list":
                br.open(("http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=" + agency + "&stopId=" + stop_number))
                soup = BeautifulSoup(br.response())
                route_direction = soup.findAll('direction')
                result = ""
                length = len(route_direction)
                if len(route_direction) > 3:
                    length =3
                for i in range(0,length):
                    route_name = route_direction[i].get('title')
                    route_prediction = route_direction[i].findAll('prediction')
                    route_time = ""
                    length1 = len(route_prediction)
                    if len(route_prediction) > 3:
                        length1 = 3
                    for j in range(0, length1):
                        route_time += str(route_prediction[j].get('minutes')) + " mins\n"
                    result += route_name + "\n" + route_time + "\n"
                return result

            else:
                if bus_number==False:
                    br.open(("http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=" + agency + "&stopId=" + stop_number))
                else:
                    br.open(("http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=" + agency + "&stopId=" + stop_number+"&routeTag="+bus_number))
                soup = BeautifulSoup(br.response())
                route_prediction = soup.findAll('prediction')
                route_time = str(route_prediction[0].get('minutes')) + " mins"
                route_direction = soup.findAll('direction')
                route_name = route_direction[0].get('title')
                return route_time + "\n" + route_name
        except:
            return "Please Try Again"


response = "2013"

number = "14164545756"
greeting = UserDB.check_user(number)
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





print result