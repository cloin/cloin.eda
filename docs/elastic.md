## Plugin:

elastic.py

## Purpose:

event-driven ansible source plugin for Elasticsearch

## Description:

Poll Elasticsearch API for matching log lines
    Retrieves matching log lines based on query. Log lines
    are then placed on the queue for evaluation by ansible
    rulebooks to execute an action based on matching condition

## Arguments:

elastic_host: path to elastic host (default: localhost)
    elastic_port: elastic port (default: 9200)
    elastic_username: basic auth username
    elastic_password: basic auth password
    elastic_index_pattern: a string or regular expression allowing you to search and analyze data across multiple related indices simultaneously
    query: query to be used to return matching log lines
    interval: seconds to wait before performing another query (default: 5)

## Example(s):

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

