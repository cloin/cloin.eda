.. _rss_module:


rss -- Event-Driven Ansible source plugin for RSS feed events
=============================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Poll multiple RSS feeds for new items

Only retrieves items that occurred after the script began executing






Parameters
----------

  feed_configs (True, list, None)
    A list of dictionaries, each representing a configuration for an RSS feed.

    Each dictionary must have a 'url' key containing the URL of the RSS feed.

    Optionally, a 'search' key can be included to filter items based on a search string present in the item's summary.

    Optionally, a 'content\_tags' key can be provided to specify the dot-notation path for content tags within each feed item. If found, a new key "content\_tags" is added to the dictionary.

    Optionally, an 'interval' key can be provided to specify the polling interval in seconds for this specific feed. If not provided, the global 'interval' value is used.


  interval (False, any, 7200)
    The default interval, in seconds, at which the script polls the feeds. This value is used when an individual 'interval' is not specified in the 'feed\_configs'.


  most_recent_item (False, bool, False)
    When True, the most recent item on the RSS feed will be used as the first event dictionary.









Examples
--------

.. code-block:: yaml+jinja

    
    - name: New Ansible blog post notifier
      hosts: localhost
      sources:
        - name: RSS feed items as events
          cloin.eda.rss:
            feed_configs:
              - name: Ansible blog
                url: https://www.ansible.com/blog/rss.xml
                search: ""
                content_tags: tags
                interval: 300
            interval: 7200
            most_recent_item: false
          filters:
            - ansible.eda.json_filter:
                exclude_keys:
                  - summary

      rules:
        - name: New EDA blog
          condition: |
            event.id is defined and
            event.content_tags is search("Event-Driven Ansible",ignorecase=true)
          action:
            debug:






Status
------





Authors
~~~~~~~

- Colin McNaughton ([@cloin](https://github.com/cloin))

