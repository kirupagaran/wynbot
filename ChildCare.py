
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


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def dispatch(intent_request):

    intent_name = intent_request['currentIntent']['name']
    sb = intent_request['currentIntent']['slots']['SuburbName']
    suburb = sb
    source = intent_request['invocationSource']
    slots = intent_request['currentIntent']['slots']
    # Dispatch to your bot's intent handlers

    if intent_name == 'ChildCare':
        if suburb is None:
            return{
                "dialogAction":{
                    "type": "ElicitSlot",
                    "message": {
                        "contentType": "PlainText",
                        "content": "Please specify the Suburb name you are trying to find Child Care Centres in Wyndham"
                    },
                    "intentName": "ChildCare",
                    "slots": slots,
                    "slotToElicit" : "SuburbName"
                }
            }

        else:
            if suburb.replace("\"","").replace(" ","").lower() in ["cocoroc","eynesbury","hopperscrossing","laverton","lavertonnorth","littleriver","mambourin","manorlakes","mountcottrell","pointcook","tarneit","quandong","truganina","werribee","werribeesouth","williamslanding","wyndhamvale"]:
                response_data = ""
                with open('/tmp/child_care.csv', 'rb') as csvfile:
                    count = 1
                    #suburb = "Little River"
                    for line in csvfile.readlines():
                        array = line.split(',')
                        first_item = array[0].replace("\"","").replace(" ","").lower()
                        if(first_item==suburb.replace("\"","").replace(" ","").lower()):
                            response_data += str(count) + ")" + array[1].replace("\"", "")+", "+array[3].replace("\"", "")+array[3].replace("\"", "")+" [Email ID - "+ array[2] + "]" + "   "
                            count+=1
                if response_data == "":
                    response_data = "There are no Child Care Centres in "+suburb
                return{
                    "dialogAction": {
                        "type": "Close",
                        "fulfillmentState": "Fulfilled",
                        "message": {
                            "contentType": "PlainText",
                            "content": response_data
                        }
                    }
                }
            else:
                return{
                "dialogAction":{
                    "type": "ElicitSlot",
                    "message": {
                        "contentType": "PlainText",
                        "content": "I could not find any matching suburb. Please enter the correct suburb name"
                    },
                    "intentName": "ChildCare",
                    "slots": slots,
                    "slotToElicit" : "SuburbName"
                }
            }
    raise Exception('Intent with name ' + intent_name + ' not supported')


""" --- Main handler --- """

s3_client = boto3.client('s3')
s3_client.download_file('wyndhamgovhack', 'child_care.csv','/tmp/child_care.csv')
#
def lambda_handler(event, context):

    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    return dispatch(event)

