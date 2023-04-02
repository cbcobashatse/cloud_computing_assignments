import boto3
# Define the client to interact with Lex
client = boto3.client('lexv2-runtime')
def lambda_handler(event, context):


   msg_from_user = event['messages'][0]
   message = msg_from_user['unstructured']['text']
 
   response = client.recognize_text(
           botId='Q3BLYHKCN2', # MODIFY HERE
           botAliasId='TSTALIASID', # MODIFY HERE
           localeId='en_US',
           sessionId='testuser',
           text=message)
  
   msg_from_lex = response.get('messages', [])
   if msg_from_lex:
      
    
       resp = {
           "messages": [
           {
           "type": "unstructured",
           "unstructured": {
           "id": "botresponse_1",
           "text": msg_from_lex[0]['content']
           }
           }
           ]
           }




       return resp
