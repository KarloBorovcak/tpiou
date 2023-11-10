"""
This module contains code for receiving events from Azure Event Hub
using the EventHubConsumerClient.
"""
import os
from azure.eventhub import EventHubConsumerClient

EVENT_HUB_CONNECTION_STR = os.getenv("EVENT_HUB_CONNECTION_STR")
EVENT_HUB_NAME = os.getenv("EVENT_HUB_NAME")
CONSUMER_GROUP = "$Default"

def on_event(partition_context, event):
    """
    Callback function for receiving events.

    Args:
        partition_context (azure.eventhub.EventContext): The context information for the partition.
        event (azure.eventhub.EventData): The received event.
    """
    context = partition_context
    print(f"Received event from partition: {context.partition_id}")
    print(event.body_as_str(encoding='UTF-8'))

def receive():
    """
    Start receiving events from the Event Hub.
    """
    # Consumer client for the event hub.
    client = EventHubConsumerClient.from_connection_string(
        conn_str=EVENT_HUB_CONNECTION_STR,
        consumer_group=CONSUMER_GROUP,
        eventhub_name=EVENT_HUB_NAME
    )
    try:
        with client:
            client.receive(on_event=on_event)
    except KeyboardInterrupt:
        print('Stopped receiving.')

if __name__ == '__main__':
    receive()
