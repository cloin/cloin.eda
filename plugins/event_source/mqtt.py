
DOCUMENTATION = r'''
module: mqtt
short_description: event-driven-ansible source plugin for mqtt
description:
    - Subscribes topic on mqtt and prints messages to ansible-rulebook
    - Test script stand-alone by exporting MQTT_HOST and MQTT_TOPIC as environment variables MQTT_HOST, MQTT_TOPIC
author: "Colin McNaughton (@cloin)"
options:
    host:
        description:
            - URL for mqtt broker
        required: true
    topic:
        description:
            - Topic to subscribe to for events
        required: true
notes:
    - This is currently only capable of basic authentication and is used so far only for demo purposes
'''

EXAMPLES = r'''
    - name: Minecraft events
      hosts: localhost
      sources:
        - cloin.eda.mqtt:
            host: localhost
            topic: messages

      rules:
        - name: New minecraft event
          condition: event.type is defined
          action:
            debug:
'''

import asyncio
import logging
import os
from typing import Any, Dict

from asyncio_mqtt import Client

async def main(queue: asyncio.Queue, args: Dict[str, Any]):
    logger = logging.getLogger()
    topic = args.get("topic")
    host = args.get("host")

    async with Client(host) as client:
        async with client.messages() as messages:
            await client.subscribe(f'{topic}/#')
            async for message in messages:
                await queue.put(message.payload.decode())

if __name__ == "__main__":
    topic = os.environ.get('MQTT_TOPIC')
    host = os.environ.get('MQTT_HOST')

    class MockQueue:
        print(f"Waiting for messages on '{topic}'...")
        async def put(self, event):
            print(event)

    asyncio.run(main(MockQueue(), {"topic": topic, "host": host}))
