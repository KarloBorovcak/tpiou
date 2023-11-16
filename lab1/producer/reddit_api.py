"""
This module contains code for interacting
with the Reddit API to get access to the API.
"""
import os
import requests

CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
SECRET_KEY = os.getenv("REDDIT_SECRET_KEY")
username = os.getenv("REDDIT_USERNAME")
password = os.getenv("REDDIT_PASSWORD")

def get_access():
    """
    Retrieves an access token from the Reddit API
    """
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)
    data = {
        'grant_type': 'password',
        'username': username,
        'password': password
    }
    headers = {'User-Agent': 'MyAPI/0.0.2'}
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)
    TOKEN = res.json()['access_token']
    headers['Authorization'] = f"bearer {TOKEN}"

    return headers
