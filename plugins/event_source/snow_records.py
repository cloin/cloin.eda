"""
new_records.py

event-driven-ansible source plugin example

Poll ServiceNow API for new records in a table
Only retrieves records created after the script began executing
This script can be tested outside of ansible-rulebook by specifying
environment variables for SN_HOST, SN_USERNAME, SN_PASSWORD, SN_TABLE

Arguments:
  - instance: ServiceNow instance (e.g. https://dev-012345.service-now.com)
  - username: ServiceNow username
  - password: ServiceNow password
  - table:    Table to watch for new records
  - query:    (optional) Records to query. Defaults to records created today
  - interval: (optional) How often to poll for new records. Defaults to 5 seconds

- name: Watch for new records
  hosts: localhost
  sources:
    - cloin.servicenow.new_records:
        instance: https://dev-012345.service-now.com
        username: ansible
        password: ansible
        table: incident
        interval: 1
  rules:
    - name: New record created
      condition: event.sys_id is defined
      action:
        debug:
"""

import asyncio
import time
import os
from typing import Any, Dict
import aiohttp

# Entrypoint from ansible-rulebook
async def main(queue: asyncio.Queue, args: Dict[str, Any]):

    instance = args.get("instance")
    username = args.get("username")
    password = args.get("password")
    table    = args.get("table")
    query    = args.get("query", "sys_created_onONToday@javascript:gs.beginningOfToday()@javascript:gs.endOfToday()")
    interval = int(args.get("interval", 5))

    start_time = time.time()
    start_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(start_time))
    printed_records = set()
    async with aiohttp.ClientSession() as session:
        auth = aiohttp.BasicAuth(login=username, password=password)
        while True:
            async with session.get(f'{instance}/api/now/table/{table}?sysparm_query={query}', auth=auth) as resp:
                if resp.status == 200:

                    records = await resp.json()
                    for record in records['result']:

                        if record['sys_updated_on'] > start_time_str and record['sys_id'] not in printed_records:
                            printed_records.add(record['sys_id'])
                            await queue.put(record)

                else:
                    print(f'Error {resp.status}')
            await asyncio.sleep(interval)


# this is only called when testing plugin directly, without ansible-rulebook
if __name__ == "__main__":
    instance = os.environ.get('SN_HOST')
    username = os.environ.get('SN_USERNAME')
    password = os.environ.get('SN_PASSWORD')
    table    = os.environ.get('SN_TABLE')

    class MockQueue:
        print(f"Waiting for events on '{table}' table...")
        async def put(self, event):
            print(event)

    asyncio.run(main(MockQueue(), {"instance": instance, "username": username, "password": password, "table": table}))
