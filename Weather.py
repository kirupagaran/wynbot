
import json
import dateutil.parser
import datetime
import time
import os
import math
import random
import logging
import boto3
import csv
import urllib

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def dispatch(intent_request):

    intent_name = intent_request['currentIntent']['name']
    source = intent_request['invocationSource']
    # Dispatch to your bot's intent handlers

    if intent_name == 'Weather':
        response1 = urllib.urlopen("http://api.openweathermap.org/data/2.5/weather?q=Werribee&APPID=9005f814a656df017dfc1b7231186fb7")
        wasteJson1 = response1.read()
        wasteJsonData1 = json.loads(wasteJson1)
        weather_desc = wasteJsonData1['weather'][0]['description']
        temp_low = wasteJsonData1['main']['temp_min']-273.15
        temp_high = wasteJsonData1['main']['temp_max']-273.15
        full_weather = "Weather Description: "+weather_desc+", Min: "+str(temp_low)+" degrees, Max: "+str(temp_high)+" degress"
        return{
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": "It is going to be "+weather_desc+" with miniumum of "+str(temp_low)+" and max of "+str(temp_high)+" degrees."
                }
            }
        }
    #raise Exception('Intent with name ' + intent_name + ' not supported')


""" --- Main handler --- """


#
def lambda_handler(event, context):

    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    return dispatch(event)

