"""
This module contains code for interacting 
with the Reddit API to retrieve top posts
from the 'dataengineering' subreddit using OAuth2 authentication.
"""
import os
import requests

ENDPOINT = 'https://oauth.reddit.com'
PATH = '/r/dataengineering/top'

CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
SECRET_KEY = os.getenv("REDDIT_SECRET_KEY")
username = os.getenv("REDDIT_USERNAME")
password = os.getenv("REDDIT_PASSWORD")

def get_data():
    """
    Retrieves top posts from the 'dataengineering' subreddit using OAuth2 authentication.

    Returns:
        dict: The JSON response containing the top posts data.
    """
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
