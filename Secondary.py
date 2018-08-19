import streaming
import time_management
from time import sleep

s= time_management.InitTime()
count = 0
while(True):
    count += 1
    if (count==2):
        time_management.Time(s.count2,s.users,s.agency,s.stop,s.sorted_time)
        count = 0
    streaming.InitStream()
    sleep(30)

