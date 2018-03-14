import mechanize
from BeautifulSoup import BeautifulSoup
import UserDB
def look_up(stop_number, bus_number, bus_agency):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Firefox')]

    br.open("http://nextride.brampton.ca/mob/SearchBy.aspx")
    br.select_form(nr=0)
    br.submit(name="ctl00$mainPanel$lbtnSearchByStop")

    br.select_form(nr=0)
    br.form['ctl00$mainPanel$searchbyStop$txtStop']=stop_number
    br.select_form(nr=0)
    br.submit(name="ctl00$mainPanel$btnGetRealtimeSchedule")
    response= br.reload()
    route_name=[]
    route_time=[]
    soup=BeautifulSoup(response.read())
    table = soup.find("table",border=1)
    result = False
    try:

        if (bus_number == False):
            for row in table.findAll('tr')[1:]:
                col = row.findAll('td')
                route_name.append(col[0].string)
                route_time.append(col[1].string)

            return str(route_name[0]) + "\n"+ str(route_time[0])
        elif(bus_number=="list"):
            str23 = ""
            for row in table.findAll('tr')[1:]:
                col = row.findAll('td')
                route_name.append((col[0].string+"\n"+col[1].string+"\n"))
            if (len(route_name)>5):
                length = 5
            else:
                length = int(len(route_name))
            for stuff in range(0,length):
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
         return "error"

response = "4037"

