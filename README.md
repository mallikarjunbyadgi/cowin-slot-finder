# cowin-slot-finder
python script to identify slots using cowin public API

This script can be run in your system which runs every 1 minute (configurable) and if it finds any slots for 18+ age group then email would be sent. 
Based on the notification one can immediate login to cowin application and book the slot.

Setup:
-	Email set up
You need to create one dummy gmail account(as sender) with less secure flag. And configure username and password in the script.
-	Age group
Configure 18 or 45. Default is 18
-	District id 
Set according to your requirement. Get Id from API mentioned in the script. Default is Karnataka, BBMP

