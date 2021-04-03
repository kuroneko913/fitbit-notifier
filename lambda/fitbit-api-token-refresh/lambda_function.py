import json
import requests
from SecretManager import SecretManager

def lambda_handler(event, context):
    sm = SecretManager('Fitbit')
    secret = sm.get()
    headers = {
        'Authorization':'Basic '+secret['BASIC_TOKEN'],
        'Content-Type':'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type':'refresh_token',
        'refresh_token':secret['REFRESH_TOKEN']
    }
    response = requests.post(
        'https://api.fitbit.com/oauth2/token', 
        headers = headers, 
        data = data
    )
    params = json.loads(response.content)
    secrets = {
        'BASIC_TOKEN': secret['BASIC_TOKEN'],
        'CLIENT_ID': secret['CLIENT_ID'],
        'CLIENT_SECRET': secret['CLIENT_SECRET'],
        'ACCESS_TOKEN': params['access_token'],
        'REFRESH_TOKEN': params['refresh_token'],
    }
    sm.update(secrets)
    
    return {
        'statusCode': 200,
        'body': 'update!!'
    }
