.. _elastic_module:


elastic -- event-driven ansible source plugin for Elasticsearch
===============================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Poll Elasticsearch API for matching log lines

Retrieves matching log lines based on query

Log lines are then placed on the queue for evaluation by ansible rulebooks to execute an action based on matching condition






Parameters
----------

  elastic_host (True, any, localhost)
    URL of Elastic host


  elastic_port (True, any, 9200)
    Port Elastic is using


  elastic_username (True, any, None)
    Username for Elastic (basic auth)


  elastic_password (True, any, None)
    Password for Elastic (basic auth)


  elastic_index_pattern (True, any, None)
    A string or regular expression allowing you to search and analyze data across multiple related indices simultaneously


  query (True, any, None)
    Query (as yaml dict) to be used to return matching log lines


  interval (False, any, 5)
    Seconds to wait before performing another query





Notes
-----

.. note::
   - This is currently only capable of basic authentication and is used so far only for demo purposes




Examples
--------

.. code-block:: yaml+jinja

    
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





Status
------





Authors
~~~~~~~

- Colin McNaughton (@cloin)

