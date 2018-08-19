import mechanize
from BeautifulSoup import BeautifulSoup
import UserDB
import sys, os
import datetime
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

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

            return "Bus Not Available. Try Again Later."

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
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return "Bus Not Available. Try Again Later."
    elif "yrt" in agency:
        now = datetime.datetime.now()

        url = "http://tripplanner.yrt.ca/hiwire?Date=Today&TimeHour=" + str(now.hour) + "&TimeMinute=" + str(
            now.minute) + "&Meridiem=p&.a=iNextBusFind&.s=uGn3PvuBC8n8bsSnsOmPmA&ShowTimes=1&NumStopTimes=5&GetSchedules=1&EndGeo=&StopAbbr=" + stop_number + "&.a=iNextBusFind"
        response = br.open(url)
        soup = BeautifulSoup(response.read())
        table = soup.find("table", attrs={'class': 'datatable'})
        route_name = []
        route_time = []
        try:

            if (bus_number == False):
                for row in table.findAll('tr')[1:]:
                    col = row.findAll('td')
                    route_name.append(col[2].string)
                    route_time.append(col[3].string)

                return str(route_name[0]) + "\n" + str(route_time[0])
            elif (bus_number == "list"):
                str23 = ""
                for row in table.findAll('tr')[1:]:
                    col = row.findAll('td')
                    route_name.append((col[2].string + "\n" + col[3].string + "\n"))
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
                    for route in col[2]:
                        test = filter(unicode.isdigit, route.string)
                        test = test[0:len(bus_number)]
                        if (bus_number == test):
                            route_name.append(col[2].string)
                            route_time.append(col[3].string)
                            result = str(route_name[0]) + "\n" + str(route_time[0])
                            break
                if (result):
                    return result
                else:
                    return ("Bus Not Available")

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

            return "Bus Not Available. Try Again Later."

