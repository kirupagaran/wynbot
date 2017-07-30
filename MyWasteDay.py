
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
    user = intent_request['currentIntent']['slots']['UserName']
    address = intent_request['currentIntent']['slots']['AddressName']

    source = intent_request['invocationSource']
    slots = intent_request['currentIntent']['slots']
    # Dispatch to your bot's intent handlers

    if intent_name == 'WasteCollectionDay':
        if user is None and address is None:
            return{
                "dialogAction":{
                    "type": "ElicitSlot",
                    "message": {
                        "contentType": "PlainText",
                        "content": "Please specify your name"
                    },
                    "intentName": "WasteCollectionDay",
                    "slots": slots,
                    "slotToElicit" : "UserName"
                }
            }
        if user is not None and address is None:
            return{
                "dialogAction":{
                    "type": "ElicitSlot",
                    "message": {
                        "contentType": "PlainText",
                        "content": "Please specify your Address"
                    },
                    "intentName": "WasteCollectionDay",
                    "slots": slots,
                    "slotToElicit" : "AddressName"
                }
            }
        if user is None and address is not None:
            return{
                "dialogAction": {
                    "type": "Close",
                    "fulfillmentState": "Fulfilled",
                    "message": {
                        "contentType": "PlainText",
                        "content": "sdf is done"
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

