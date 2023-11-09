from azure.eventhub import EventHubConsumerClient
import os

# Connection string - primary key of the Event Hubs namespace.
EVENT_HUB_CONNECTION_STR = os.getenv("EVENT_HUB_CONNECTION_STR")
EVENT_HUB_NAME = os.getenv("EVENT_HUB_NAME")
CONSUMER_GROUP = "$Default"

def on_event(partition_context, event):
    print(event.body_as_str(encoding='UTF-8'))

def receive():
    # Create a consumer client for the event hub.
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