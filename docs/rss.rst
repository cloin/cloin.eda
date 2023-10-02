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

    
    - name: Respond to RSS feed events
      hosts: all
      sources:
        - cloin.eda.rss:
            feed_configs:
              - url: "https://www.ansible.com/blog/rss.xml"
                search: "python"
                content_tags: "tags"
                interval: 300
              - url: "http://example.com/rss2"
            interval: 7200
            most_recent_item: True
      rules:
        - name: Catch all RSS feed items
          condition: event.link is defined
          action:
            debug:





Status
------





Authors
~~~~~~~

- Colin McNaughton (@cloin)

