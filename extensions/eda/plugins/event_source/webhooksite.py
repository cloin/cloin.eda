DOCUMENTATION = r'''
module: webhooksite
short_description: Event-Driven Ansible source plugin for Webhook.site events
description:
    - Poll Webhook.site API for new requests
    - Only retrieves requests that occurred after the script began executing
    - This script can be tested outside of ansible-rulebook by specifying environment variables for WEBHOOK_SITE_TOKEN, WEBHOOK_SITE_API_URL, and INTERVAL
author: "Colin McNaughton (@cloin)"
options:
    token:
        description:
            - Your Webhook.site token. This is the last part of the URL when viewing your requests
        required: true
    api_url:
        description:
            - The URL for the Webhook.site API
        required: false
        default: "https://webhook.site/token/{token}/requests"
    interval:
        description:
            - The interval, in seconds, at which the script polls the API (mind the rate limit!)
        required: false
        default: 15
    skip_first_poll:
        description:
            - Whether to skip returning items on the first poll
        required: false
        default: true
'''

EXAMPLES = r'''
- name: webhook.site events
  hosts: localhost
  sources:
    - name: Webhook.site POSTs as events
      webhooksite:
        token: "d40e1855-5555-5555-5555-5566c1791540"
        api_url: "https://webhook.site/token/{token}/requests"
        interval: 15
        skip_first_poll: true

  rules:
    - name: R1 - New webhook.site POST with content
      condition: |
        event.content.foo == "bar"
      action:
        debug:
'''

import aiohttp
import asyncio
import os
import json
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def fetch_webhook_site_requests(session, api_url, start_time, token):
    params = {
        "created_at": [f'"{start_time.strftime("%Y-%m-%d %H:%M:%S")}" TO *']
    }
    headers = {"Token": token}
    try:
        async with session.get(api_url, params=params, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                logging.error(f"HTTP Status Code: {response.status}")
                logging.error("Response Text: %s", await response.text())
                return None
    except aiohttp.ClientError as e:
        logging.error(f"Request failed: {e}")
        return None

async def main(queue: asyncio.Queue, args: dict):
    interval = int(args.get("interval", 15))
    token = args.get("token")
    api_url = args.get("api_url", "https://webhook.site/token/{token}/requests").format(token=token)
    skip_first_poll = args.get("skip_first_poll", True)

    async with aiohttp.ClientSession() as session:
        start_time = datetime.utcnow() - timedelta(minutes=5)
        processed_requests = set()
        first_poll = True

        while True:
            response_data = await fetch_webhook_site_requests(session, api_url, start_time, token)

            if response_data:
                new_requests = response_data.get('data', [])
                if first_poll:
                    logging.info("First poll URL: %s", api_url)
                    logging.info("Number of requests discovered: %d", len(new_requests))

                for request in new_requests:
                    request_id = request.get('uuid')
                    if request_id and request_id not in processed_requests:
                        processed_requests.add(request_id)
                        if not (first_poll and skip_first_poll):
                            try:
                                request['content'] = json.loads(request.get('content', '{}'))
                            except json.JSONDecodeError:
                                logging.error("Failed to parse JSON content")
                            else:
                                await queue.put(request)

            first_poll = False
            await asyncio.sleep(interval)
            start_time = datetime.utcnow() - timedelta(minutes=5)

if __name__ == "__main__":
    args = {
        "token": os.getenv("WEBHOOK_SITE_TOKEN"),
        "api_url": os.getenv("WEBHOOK_SITE_API_URL", "https://webhook.site/token/{token}/requests"),
        "interval": os.getenv("INTERVAL", "15"),
        "skip_first_poll": os.getenv("SKIP_FIRST_POLL", "true").lower() == "true",
    }

    class MockQueue:
        async def put(self, event):
            logging.info(event)

    asyncio.run(main(MockQueue(), args))
