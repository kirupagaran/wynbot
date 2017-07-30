
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
    if intent_name == 'PublicToilets':
        if suburb is None:
            return{
                "dialogAction":{
                    "type": "ElicitSlot",
                    "message": {
                        "contentType": "PlainText",
                        "content": "Please specify the Suburb name in Wyndham"
                    },
                    "intentName": "PublicToilets",
                    "slots": slots,
                    "slotToElicit" : "SuburbName"
                }
            }
        else:
            if suburb.replace("\"","").replace(" ","").lower() in ["cocoroc","eynesbury","hopperscrossing","laverton","lavertonnorth","littleriver","mambourin","manorlakes","mountcottrell","pointcook","tarneit","quandong","truganina","werribee","werribeesouth","williamslanding","wyndhamvale"]:
                toilets_data = ""
                with open('/tmp/toilet.csv', 'rb') as csvfile:
                    count = 1
                    #suburb = "Little River"
                    for line in csvfile.readlines():
                        array = line.split(',')
                        first_item = array[3].replace("\"","").replace(" ","").lower()
                        if(first_item==suburb.replace("\"","").replace(" ","").lower()):
                            toilets_data += str(count)+")"+array[1]+","+array[2].replace("\"","")+"   "
                            count+=1
                if toilets_data == "":
                    toilets_data = "There are no toilets in the requested suburb"
                return{
                    "dialogAction": {
                        "type": "Close",
                        "fulfillmentState": "Fulfilled",
                        "message": {
                            "contentType": "PlainText",
                            "content": toilets_data
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
                    "intentName": "PublicToilets",
                    "slots": slots,
                    "slotToElicit" : "SuburbName"
                }
            }
    """PLAY GROUNDS CODE """
    if intent_name == 'PlayGrounds':
        if suburb is None:
            return{
                "dialogAction":{
                    "type": "ElicitSlot",
                    "message": {
                        "contentType": "PlainText",
                        "content": "Enter the Suburb name in Wyndham"
                    },
                    "intentName": "PublicToilets",
                    "slots": slots,
                    "slotToElicit" : "SuburbName"
                }
            }
        else:
            if suburb.replace("\"","").replace(" ","").lower() in ["cocoroc","eynesbury","hopperscrossing","laverton","lavertonnorth","littleriver","mambourin","manorlakes","mountcottrell","pointcook","tarneit","quandong","truganina","werribee","werribeesouth","williamslanding","wyndhamvale"]:
                toilets_data = ""
                with open('/tmp/toilet.csv', 'rb') as csvfile:
                    count = 1
                    #suburb = "Little River"
                    for line in csvfile.readlines():
                        array = line.split(',')
                        first_item = array[3].replace("\"","").replace(" ","").lower()
                        if(first_item==suburb.replace("\"","").replace(" ","").lower()):
                            toilets_data += str(count)+")"+array[1]+","+array[2].replace("\"","")+"   "
                            count+=1
                if toilets_data == "":
                    toilets_data = "There are no play grounds in "+suburb
                return{
                    "dialogAction": {
                        "type": "Close",
                        "fulfillmentState": "Fulfilled",
                        "message": {
                            "contentType": "PlainText",
                            "content": toilets_data
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
                    "intentName": "PublicToilets",
                    "slots": slots,
                    "slotToElicit" : "SuburbName"
                }
            }
    raise Exception('Intent with name ' + intent_name + ' not supported')


""" --- Main handler --- """

s3_client = boto3.client('s3')
s3_client.download_file('wyndhamgovhack', 'toilets.csv','/tmp/toilet.csv')
#
def lambda_handler(event, context):

    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    return dispatch(event)

