import os
import httpx
from dotenv import load_dotenv
from ms_graph import get_access_token, MS_GRAPH_BASE_URL

def main():
    load_dotenv()
    APPLICATION_ID = os.getenv('APPLICATION_ID')
    CLIENT_SECRET= os.getenv('CLIENT_SECRET')
    SCOPES = ['User.Read', 'Mail.ReadWrite']

    endpoint = f'{MS_GRAPH_BASE_URL}/me/messages'

    try:
        access_token =  get_access_token(
            application_id = APPLICATION_ID,
            client_secret=  CLIENT_SECRET,
            scopes= SCOPES
        )
        headers= {
            'Authorization': 'Bearer ' + access_token
        }
        for i in range(0,4,2):
            params = {
                    '$top': 10,
                    '$select': '*',
                    '$skip': i,
                    '$orderby': 'receivedDateTime desc'
                }
            response = httpx.get(endpoint, headers=headers, params=params, timeout=10.0)

            if response.status_code != 200:
                raise Exception(f'Failed to retrieve emails: {response.text}')

            json_response = response.json()

            for mail_message  in json_response.get('value',[]):
                print('Subject:', mail_message['subject'])
                print('From:', mail_message['from']['emailAddress']['address'])
                print('Is Read:', mail_message['isRead'])
                print()
    except httpx.HTTPStatusError as e:
        print(f'HTTP Error: {e}')
    except Exception as e:
        print(f'Error: {e}')

main()
