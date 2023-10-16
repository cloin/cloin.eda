# pubsub_plugin.py

"""
An ansible-rulebook event source plugin for Google Cloud Pub/Sub.

Arguments:
  - project_id: Google Cloud Project ID
  - subscription_id: Google Cloud Pub/Sub subscription ID
  - credentials: Path to the service account key file

Examples:
  sources:
    - pubsub:
        project_id: "your-gcp-project-id"
        subscription_id: "your-subscription-id"
        credentials: "/path/to/service-account-key.json"
"""

import asyncio
from google.cloud import pubsub_v1
from google.oauth2.service_account import Credentials
from typing import Any, Dict


async def pubsub_callback(message, queue: asyncio.Queue):
    await queue.put(
        {
            "pubsub": {
                "message_id": message.message_id,
                "data": message.data.decode("utf-8"),
                "attributes": message.attributes,
            }
        }
    )
    message.ack()


async def main(queue: asyncio.Queue, args: Dict[str, Any]):
    project_id = args.get("project_id")
    subscription_id = args.get("subscription_id")
    credentials_path = args.get("credentials")

    credentials = Credentials.from_service_account_file(credentials_path)
    subscriber = pubsub_v1.SubscriberClient(credentials=credentials)
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def wrapped_callback(message):
        asyncio.create_task(pubsub_callback(message, queue))

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=wrapped_callback)
    print(f"Listening for messages on {subscription_path}..\n")

    try:
        await streaming_pull_future.result()
    except asyncio.CancelledError:
        streaming_pull_future.cancel()
        print(f"Cancelled listening to {subscription_path}.")

if __name__ == "__main__":

    class MockQueue:
        async def put(self, event):
            print(event)

    mock_arguments = {
        "project_id": "your-gcp-project-id",
        "subscription_id": "your-subscription-id",
        "credentials": "/path/to/service-account-key.json",
    }
    asyncio.run(main(MockQueue(), mock_arguments))
