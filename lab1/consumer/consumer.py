"""
This module contains code for receiving events from Azure Event Hub
using the EventHubConsumerClient.
"""
import os
import json
from datetime import datetime
from azure.eventhub import EventHubConsumerClient
from azure.storage.filedatalake import DataLakeServiceClient

# Event Hub connection string and name.
EVENT_HUB_CONNECTION_STR = os.getenv("EVENT_HUB_CONNECTION_STR")
EVENT_HUB_NAME = os.getenv("EVENT_HUB_NAME")
CONSUMER_GROUP = "$Default"

# Azure Data Lake Storage connection string and name.
STORAGE_ACCOUNT_NAME = os.getenv("STORAGE_ACCOUNT_NAME")
STORAGE_ACCOUNT_CONNECTION_STR = os.getenv("STORAGE_ACCOUNT_CONNECTION_STR")
FILE_SYSTEM_NAME = "redditdata"

def save_to_datalake(data, formatted_date):
    """
    Saves the data to Azure Data Lake Storage.
    """
    # Create a DataLakeServiceClient object.
    service_client = DataLakeServiceClient.from_connection_string(
        conn_str=STORAGE_ACCOUNT_CONNECTION_STR
    )

    # Get a reference to a file system.
    file_system_client = service_client.get_file_system_client(file_system=FILE_SYSTEM_NAME)

    # Get a reference to a directory.
    directory_client = file_system_client.get_directory_client(formatted_date)

    # Create the directory if it doesn't exist.
    directory_client.create_directory()

    # Get a reference to a file.
    file_client = directory_client.get_file_client(f"{data['id']}.json")

    # Create the file if it doesn't exist.
    file_client.create_file()

    # Append data to the file.
    file_client.append_data(json.dumps(data), offset=0, length=len(json.dumps(data)))

    # Flush data to the file.
    file_client.flush_data(len(json.dumps(data)))


def on_event(partition_context, event):
    """
    Callback function for receiving events.

    Args:
        partition_context (azure.eventhub.EventContext): The context information for the partition.
        event (azure.eventhub.EventData): The received event.
    """
    context = partition_context
    print(f"Received event from partition: {context.partition_id}")

    data = json.loads(event.body_as_str(encoding='UTF-8'))
    created_utc = datetime.fromtimestamp(data['created_utc'])
    formatted_date = created_utc.strftime('%Y/%m/%d/%H/%M')

    save_to_datalake(data, formatted_date)

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
