import datetime
import requests
import smtplib, ssl
from email.message import EmailMessage
import time

MIN_AGE = 18
DISTRICT_ID = 294 #BBMP in Karnataka

def send_email(message):

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "sender_email@gmail.com"  # Enter your address
    receiver_email = "receiver_email@gmail.com"  # Enter receiver address
    password = "password" # Enter password of sender email address


    msg = EmailMessage()
    msg.set_content(message)

    msg['Subject'] = 'Cowin-app slots availability'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.send_message(msg)

    #trouble shooting : in case if smpt unble to login then follow the below step in the link
    #https://www.google.com/settings/security/lesssecureapps

def filter_cowin_slots():


    #https://cdn-api.co-vin.in/api/v2/admin/location/districts/16
    #16 is the id for karnataka

    #https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=294&date=03-06-2021
    today_date = datetime.datetime.today().strftime('%d-%m-%Y')
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
    calendarByDistrict_url = f"{url}?district_id={DISTRICT_ID}&date={today_date}"

    r=requests.get(calendarByDistrict_url, headers={"accept":"application\json", "Accept-Language" : "hi_IN"})

    if(r.status_code != 200):
        print(f"ERROR status code: {r.status_code}")
        exit()

    data = r.json()
    centers = list(data.values())[0]
    message = []
    for center in centers:
        sessions = center["sessions"]
        session_available = list(filter(lambda x: (x["min_age_limit"] == MIN_AGE and x["available_capacity_dose1"] > 0 ), sessions))
        for session in session_available:
            vacinetype= str(session["vaccine"])
            center_name =center["name"]
            date = str(session["date"])
            msg= (f"{vacinetype} available in {center_name} for the date {date}")
            print(msg)
            message.append(msg)

    if len(message) > 0:
        send_email("\n".join(message))
        print("Found some slots")
    else:
        print("Not found any slots")


def main():
    while(True):
        filter_cowin_slots()
        time.sleep(60)


if __name__ == "__main__":
    main()


