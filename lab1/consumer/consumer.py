from azure.eventhub import EventHubConsumerClient

EVENT_HUB_CONNECTION_STR = "Endpoint=sb://ns-lab1.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=uGupt1A2qiM1uljE6IvljLwXgjDuB3Zgs+AEhF7fMYE="
EVENT_HUB_NAME = "eh-lab1"
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