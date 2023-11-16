"""
This module contains code for asynchronously
retrieving data from the Reddit API
and sending it to an Azure Event Hub using the EventHubProducerClient.
"""
import os
import requests
import asyncio
import json
from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient
from reddit_api import get_access

EVENT_HUB_CONNECTION_STR = os.getenv("EVENT_HUB_CONNECTION_STR")
EVENT_HUB_NAME = os.getenv("EVENT_HUB_NAME")
ENDPOINT = 'https://oauth.reddit.com'
PATH = '/r/dataengineering/top'

async def run():
    """
    Asynchronously retrieves data from the Reddit API, creates an EventHubProducerClient,
    creates a batch of events from the Reddit data, and sends the batch to the Azure Event Hub.
    """
    headers = get_access()
    after = None

    for i in range(100):	
        # Send a GET request to the Reddit API to retrieve the top posts from the past month.
        params = {'t': 'all', 'limit': 10, 'after': after}
        res = requests.get(f'{ENDPOINT}{PATH}', headers=headers, params=params)
        data = res.json()

        if 'data' not in data or 'children' not in data['data']:
            break

        # Create a producer client to send messages to the event hub.
        # Specify a connection string to your event hubs namespace and
        # the event hub name.
        producer = EventHubProducerClient.from_connection_string(
            conn_str=EVENT_HUB_CONNECTION_STR, eventhub_name=EVENT_HUB_NAME
        )

        async with producer:
            # Create a batch.
            event_data_batch = await producer.create_batch()

            # Add events to the batch.
            for post in data['data']['children']:
                event_data_batch.add(EventData(json.dumps(post['data'])))

            # Send the batch of events to the event hub.
            await producer.send_batch(event_data_batch)
        
        after = data['data']['after']


if __name__ == '__main__':
    """
    Run the asynchronous 'run()' function using asyncio.run().
    """
    asyncio.run(run())

    # Infinite loop to keep the program running.
    while True:
        pass
