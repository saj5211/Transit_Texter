import mechanize
from BeautifulSoup import BeautifulSoup
import UserDB
import sys, os
import datetime

br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Firefox')]
now = datetime.datetime.now()
stop = "2014"
url = "http://tripplanner.yrt.ca/hiwire?Date=Today&TimeHour=" +str(now.hour) + "&TimeMinute=" + str(now.minute) + "&Meridiem=p&.a=iNextBusFind&.s=uGn3PvuBC8n8bsSnsOmPmA&ShowTimes=1&NumStopTimes=5&GetSchedules=1&EndGeo=&StopAbbr=" + stop +"&.a=iNextBusFind"
response = br.open(url)
soup = BeautifulSoup(response.read())
table = soup.find("table",attrs={'class':'datatable'})
route_name = ""
route_time = ""

for row in table.findAll('tr')[1:]:
    col =  row.findAll('td')
    print col[2].string
    print col[3].string


