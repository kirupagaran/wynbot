
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
    source = intent_request['invocationSource']
    # Dispatch to your bot's intent handlers

    if intent_name == 'AboutWyndham':
        return{
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": "PROFILE: The City is located on the western edge of Melbourne and covers an area of 542km² and features 27.4km of coastline. The city features major tourism attractions including the Werribee Park and Mansion, State Rose Garden, Werribee Open Range Zoo, Equestrian Centre, Harbour Marina, Point Cook Coastal Park and RAAF museum; and the Western Treatment Plant. It is home to major recreation and leisure facilities including AquaPulse and Eagle Stadium. The key industrial precincts are Laverton North and Truganina and the key industries are manufacturing and logistics. The professional and commercial sector includes Victoria University, CSIRO Food Innovation Centre and the University of Melbourne Veterinary Clinic and Hospital. Wyndham is a designated growth area of Melbourne, currently ranked as the third fastest growing local government area in Victoria. Wyndham has a growing and diverse population and growth has been rapid and forecasts indicate the population will be in excess of 330,000 by 2031. LOCALITIES: Cocoroc, Eynesbury, Hoppers Crossing, Laverton, Laverton North, Laverton RAAF, Little River, Mambourin, Mount Cottrell, Point Cook, Quandong, Tarneit, Truganina, Werribee, Werribee South, Williams Landing and Wyndham Vale."
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

