"""
## Plugin:
    nextdns.py

## Purpose
    An ansible-rulebook event source plugin for NextDNS logs

## Description:
    Uses the NextDNS API to subscribe to a SSE event stream
    for the logs of a specific profile and use these as events
    in Event-Driven Ansible

## Arguments:
    api_key: Your NextDNS API key
    profile_id: Your NextDNS profile ID

## Examples:
    - name: NextDNS event stream
        hosts: localhost
        sources:
            - cloin.eda.nextdns:
                profile_id: ""
                api_key: ""
"""

import asyncio
import aiohttp
import json
from aiohttp_sse_client import client as sse_client
from typing import Any, Dict


async def main(queue: asyncio.Queue, args: Dict[str, Any]):
    profile_id = args["profile_id"]
    api_key = args["api_key"]

    if not profile_id or not api_key:
        print("Please specify both the API key and profile ID")
        return

    async with aiohttp.ClientSession() as session:
        # Test API key and profile ID
        test_url = f'https://api.nextdns.io/profiles/{profile_id}/analytics/status'
        headers = {'X-Api-Key': api_key}

        try:
            async with session.get(test_url, headers=headers) as response:
                if response.status == 403:
                    print("Access Forbidden: Invalid API key or profile ID")
                    return
                elif response.status != 200:
                    print(f"Unexpected error: {response.status}")
                    return
                
                response_data = await response.json()
                print(response_data)
                
        except aiohttp.ClientError as e:
            print(f"Connection error: {e}")
            return

        # Process logs
        nextdns_api_url = f'https://api.nextdns.io/profiles/{profile_id}/logs/stream'

        async with sse_client.EventSource(nextdns_api_url, headers=headers) as client:
            async for event in client:
                event_data = json.loads(event.data)
                await queue.put(dict(nextdns=dict(log=event_data)))


if __name__ == "__main__":

    class MockQueue:
        async def put(self, event):
            print(event)

    mock_arguments = dict(profile_id="", api_key="")
    asyncio.run(main(MockQueue(), mock_arguments))
