# Transit Texter
-----

#### Texter is a Text-Messaging Service that provides users with realtime information of when the next bus is arriving. 
##
##
## Features

  - Get Realtime Next Bus Information 
  - Get Information For Specific Bus
  - List All Busses Arriving at the Stop
##
##
## QuickStart Commands
  - Next bus time --> **[stop#]**
  - Get specific bus time --> **[stop#] [bus#]**
  - Get list of all busses --> **[stop#] list**
  - Get bus info from another agency --> **[agency] [stop#]**
  - Change default agency --> **default [agency]**
##
##
## Supported Cities
- Brampton Transit [bram]
- Toronto Transit Commission [ttc]
##
##
## API's & Services Used:
##
##
![alt text](data:image/png;base64,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)

![alt](https://firebase.google.com/downloads/brand-guidelines/PNG/logo-standard.png  "firebase")
