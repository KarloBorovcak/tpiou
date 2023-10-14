import requests
import json

ENDPOINT = 'https://oauth.reddit.com'
PATH = '/r/dataengineering/top'

with open('reddit_cred.json', 'r') as f:
    credentials = json.load(f)
    CLIENT_ID = credentials['client_id']
    SECRET_KEY = credentials['secret_key']
    username = credentials['username']
    password = credentials['password']

def get_data():
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)
    data = {
        'grant_type': 'password',
        'username': username,
        'password': password
    }
    headers = {'User-Agent': 'MyAPI/0.0.1'}
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)
    TOKEN = res.json()['access_token']
    headers['Authorization'] = f"bearer {TOKEN}"

    res = requests.get(ENDPOINT + PATH, headers=headers, params={'t': 'all', 'limit': 10})
    return res.json()

# Check API response
# if res.status_code == 200:
#     data = res.json()
    
#     for post in data['data']['children']:
#         print(post['data']['title'])
# else:
    
#     print(f"Error: {res.status_code}")