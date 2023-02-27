import json
import boto3


def lambda_handler(event, context):
   # TODO implement


   bot = event['bot']['name']
   slots = event['sessionState']['intent']['slots']
   intent = event['sessionState']['intent']['name']
   response = {
       "sessionState":{
           "dialogAction":{
               "type": "Delegate"
           },
           "intent":{
               'name': intent,
               'slots': slots
           }
       }
   }


   if event['invocationSource'] == 'FulfillmentCodeHook':
       client = boto3.client("sqs")
       response = {
           "sessionState": {
               "dialogAction": {
                   "type": "Close"
               },
               "intent": {
                   "name": intent,
                   "slots": slots,
                   "state": "Fulfilled"
               }
           },
           "messages": [
               {
                   "contentType": "PlainText",
                   "content": "You’re all set. Expect my suggestions shortly! Have a good day."
               }
           ]
       }
       slot_info = {}
       slot_info["Location"] = slots['Location']['value']['interpretedValue']
       slot_info["Cuisine"] = slots['Cuisine']['value']['interpretedValue']
       slot_info["DiningDate"] = slots['DiningDate']['value']['interpretedValue']
       slot_info["DiningTime"] = slots['DiningTime']['value']['interpretedValue']
       slot_info["NumberOfPeople"] = slots['NumberOfPeople']['value']['interpretedValue']
       slot_info["Email"] = slots['Email']['value']['interpretedValue']
       message = client.send_message(
       QueueUrl= "https://sqs.us-east-1.amazonaws.com/064833673922/Q1",
       MessageBody= json.dumps(slot_info)
       )
      
      




   return response


