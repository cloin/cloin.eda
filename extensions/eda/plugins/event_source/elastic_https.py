
DOCUMENTATION = r'''
module: elastic
short_description: event-driven ansible source plugin for Elasticsearch
description:
    - Poll Elasticsearch API for matching log lines
    - Retrieves matching log lines based on query
    - Log lines are then placed on the queue for evaluation by ansible rulebooks to execute an action based on matching condition
author: "Colin McNaughton (@cloin)"
options:
    elastic_host:
        description:
            - URL of Elastic host
        required: true
        default: localhost
    elastic_port:
        description:
            - Port Elastic is using
        required: true
        default: 9200
    elastic_username:
        description:
            - Username for Elastic (basic auth)
        required: true
    elastic_password:
        description:
            - Password for Elastic (basic auth)
        required: true
    elastic_index_pattern:
        description:
            - A string or regular expression allowing you to search and analyze data across multiple related indices simultaneously
        required: true
    query:
        description:
            - Query (as yaml dict) to be used to return matching log lines
        required: true
    interval:
        description:
            - Seconds to wait before performing another query
        required: false
        default: 5
notes:
    - This is currently only capable of basic authentication and is used so far only for demo purposes
'''

EXAMPLES = r'''
- name: Elastic events
    hosts: localhost
    sources:
    - cloin.eda.elastic:
        elastic_host: elasticsearch
        elastic_port: 9200
        elastic_username: elastic
        elastic_password: elastic!
        elastic_index_pattern: filebeat-*
        query: |
        term:
            container.name.keyword: nginx
        interval: 5
'''
import asyncio
from datetime import datetime
from elasticsearch import AsyncElasticsearch
from dateutil.parser import parse
from typing import Any, Dict
import yaml
from urllib.parse import urlparse

async def main(queue: asyncio.Queue, args: Dict[str, Any]):
    elastic_host = args.get("elastic_host", "http://localhost")  # Default to http://
    elastic_port = args.get("elastic_port", 9200)  # Default port
    elastic_username = args.get("elastic_username", "elastic")
    elastic_password = args.get("elastic_password", "elastic!")
    elastic_index_pattern = args.get("elastic_index_pattern", "filebeat-*")
    interval = args.get("interval", 5)
    query = args.get("query", "term:\n  container.name.keyword: nginx")


    elastic_query = yaml.safe_load(query)

    async with AsyncElasticsearch([f"https://{elastic_host}:{elastic_port}"], http_auth=(elastic_username, elastic_password)) as es:
        # Set the initial search_after value to the current timestamp
        search_after = datetime.utcnow()

        while True:
            sort = [
                {
                    "@timestamp": {
                        "order": "asc"
                    }
                }
            ]

            # Run the query
            response = await es.search(
                index=elastic_index_pattern,
                query=elastic_query,
                sort=sort,
                search_after=[search_after.isoformat()],
                size=1000
            )

            # Process the results
            for hit in response['hits']['hits']:
                log_entry = hit["_source"]
                await queue.put(log_entry)

                # Update the search_after value to the current log entry's timestamp
                search_after = parse(log_entry["@timestamp"])

            # Wait before running the query again
            await asyncio.sleep(interval)

if __name__ == "__main__":

    class MockQueue:
        async def put(self, event):
            print(event)

    mock_arguments = {
        "elastic_host": "https://10.44.5.106",  # You can set "http://" or "https://" as needed
        "elastic_port": 9200,
        "elastic_username": "elastic",
        "elastic_password": "your_password_here",
        "elastic_index_pattern": "filebeat-*",
        "query": "term:\n  container.name.keyword: nginx",
        "interval": 5
    }
    asyncio.run(main(MockQueue(), mock_arguments))
