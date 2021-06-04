import json

import datetime
import requests
import time
import boto3

MIN_AGE = 18
DISTRICT_ID = 294 #BBMP in Karnataka


def send_sns_topic(message):

    sns = boto3.client('sns')
    # Publish a simple message to the specified SNS topic
    response = sns.publish(
        TopicArn='arn', #Confugure ARN
        Message=message,
        Subject="Cowin-app slots availability"
    )

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
        send_sns_topic("\n".join(message))
        print("Found some slots")
    else:
        print("Not found any slots")


def lambda_handler(event, context):
    filter_cowin_slots()



