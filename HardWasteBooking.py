
import json
import dateutil.parser
import datetime
import time
import os
import math
import random
import logging
import csv
import urllib


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def GoogGeoAPI(address,api="AIzaSyADvZNn0iKbxLva55y72LrQ9d7BzHWXBTc",delay=0):
    base = r"https://maps.googleapis.com/maps/api/geocode/json?"
    addP = "address=" + address.replace(" ","+")
    restrictions = "sensor=false&components=country:AU"
    GeoUrl = base + addP + "&key=" + api +"&restrictions"
    response = urllib.urlopen(GeoUrl)
    jsonRaw = response.read()
    jsonData = json.loads(jsonRaw)
    if jsonData['status'] == 'OK':
        resu = jsonData['results'][0]
        finList = [resu['formatted_address'],resu['geometry']['location']['lat'],resu['geometry']['location']['lng']]
    else:
        finList = [None,None,None]
    time.sleep(delay) #in seconds
    return finList

def dispatch(intent_request):

    intent_name = intent_request['currentIntent']['name']
    address = intent_request['inputTranscript']
    suburb = intent_request['currentIntent']['slots']['SuburbName']
    source = intent_request['invocationSource']
    slots = intent_request['currentIntent']['slots']
    # Dispatch to your bot's intent handlers

    if intent_name == 'HardWasteBooking':
        if suburb is not None:
            if address is not None:
                geoR = GoogGeoAPI(address=address+", VIC AUSTRALIA")
                if(geoR[1] is not None and geoR[2] is not None):
                    url = 'http://wyndev.com.au/mywyndham/JSON/show_closest_feed.php?lat='+str(geoR[1])+'&lng='+str(geoR[2])
                    response = urllib.urlopen(url)
                    wasteJson = response.read()
                    wasteJsonData = json.loads(wasteJson)
                    recycle = wasteJsonData['waste_collection_information']['Recycle']
                    greenwaste = wasteJsonData['waste_collection_information']['Green_Waste']
                    waste = wasteJsonData['waste_collection_information']['Waste']
                    if waste is None or recycle is None or greenwaste is None:
                        return{
                            "dialogAction":{
                                "type": "ElicitSlot",
                                "message": {
                                    "contentType": "PlainText",
                                    "content": "Sorry, This address is either not in Wyndham council or no bin date is available. Can you try with correct address please ?"
                                },
                                "intentName": "WasteCollectionDay",
                                "slots": slots,
                                "slotToElicit" : "SuburbName"
                            }
                        }
                    else:
                        wasteDay = "RECYCLE BIN: "+recycle+", GREENWASTE BIN: "+greenwaste+", RUBBISH BIN: "+waste
                        return{
                            "dialogAction": {
                                "type": "Close",
                                "fulfillmentState": "Fulfilled",
                                "message": {
                                    "contentType": "PlainText",
                                    "content": "I was able to find the collection dates for you:                     "+wasteDay+" CAN I HELP YOU WITH ANYTHING ELSE ?"
                                }
                            }
                        }
                else:
                    return{
                        "dialogAction":{
                            "type": "ElicitSlot",
                            "message": {
                                "contentType": "PlainText",
                                "content": "Sorry, I cannot recognise your address. Can you try again please ?"
                            },
                            "intentName": "WasteCollectionDay",
                            "slots": slots,
                            "slotToElicit" : "SuburbName"
                        }
                    }

        else:
            return{
                "dialogAction":{
                    "type": "ElicitSlot",
                    "message": {
                        "contentType": "PlainText",
                        "content": "Can you specify your Address please ?"
                    },
                    "intentName": "WasteCollectionDay",
                    "slots": slots,
                    "slotToElicit" : "SuburbName"
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



