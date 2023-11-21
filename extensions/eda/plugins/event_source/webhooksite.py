DOCUMENTATION = r'''
module: webhooksite_events
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
        default: 10
    skip_first_poll:
        description:
            - Whether to skip returning items on the first poll
        required: false
        default: true
'''

import aiohttp
import asyncio
import os
import json
from datetime import datetime, timedelta

async def fetch_webhook_site_requests(session, api_url, start_time, token):
    params = {
        "created_at": [f'"{start_time.strftime("%Y-%m-%d %H:%M:%S")}" TO *']
    }
    headers = {"Token": token}
    try:
        async with session.get(api_url, params=params, headers=headers, ssl=False) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"HTTP Status Code: {response.status}")
                print("Response Text:", await response.text())
                return None
    except aiohttp.ClientError as e:
        print(f"Request failed: {e}")
        return None

async def main(queue: asyncio.Queue, args: dict):
    interval = int(args.get("interval", 10))
    token = args.get("token")
    api_url = args.get("api_url", "https://webhook.site/token/{token}/requests").format(token=token)
    skip_first_poll = args.get("skip_first_poll", True)

    async with aiohttp.ClientSession() as session:
        start_time = datetime.utcnow() - timedelta(minutes=5)
        processed_requests = set()
        first_poll = True

        while True:
            response = await fetch_webhook_site_requests(session, api_url, start_time, token)

            if response and 'data' in response:
                for request in response['data']:
                    request_id = request.get('uuid')
                    if request_id not in processed_requests:
                        if not (first_poll and skip_first_poll):
                            # Parse the 'content' field from string to dictionary
                            if 'content' in request and request['content']:
                                try:
                                    request['content'] = json.loads(request['content'])
                                except json.JSONDecodeError:
                                    print("Failed to parse JSON content")
                                    continue
                            await queue.put(request)
                        processed_requests.add(request_id)

            first_poll = False
            await asyncio.sleep(interval)
            start_time = datetime.utcnow() - timedelta(minutes=5)

if __name__ == "__main__":
    args = {
        "token": os.getenv("WEBHOOK_SITE_TOKEN"),
        "api_url": os.getenv("WEBHOOK_SITE_API_URL", "https://webhook.site/token/{token}/requests"),
        "interval": os.getenv("INTERVAL", "10"),
        "skip_first_poll": os.getenv("SKIP_FIRST_POLL", "true").lower() == "true",
    }

    class MockQueue:
        async def put(self, event):
            print(event)

    asyncio.run(main(MockQueue(), args))
