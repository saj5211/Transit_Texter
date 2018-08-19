from selenium import webdriver
from time import sleep
import UserDB
stop = str(1960)
driver = webdriver.PhantomJS()
driver.get("http://www4.mississauga.ca/PlanATrip/NextDepartures?ShowOptions=false&StopFilterIdentifier=&StopFilterType=&StopIdentifier="+stop)
p_element = driver.find_element_by_id(id_='intro-text')
print(p_element.text)


