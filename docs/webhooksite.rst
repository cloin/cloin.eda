.. _webhooksite_module:


webhooksite -- Event-Driven Ansible source plugin for Webhook.site events
=========================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Poll Webhook.site API for new requests

Only retrieves requests that occurred after the script began executing

This script can be tested outside of ansible-rulebook by specifying environment variables for WEBHOOK\_SITE\_TOKEN, WEBHOOK\_SITE\_API\_URL, and INTERVAL






Parameters
----------

  token (True, any, None)
    Your Webhook.site token. This is the last part of the URL when viewing your requests


  api_url (False, any, https://webhook.site/token/{token}/requests)
    The URL for the Webhook.site API


  interval (False, any, 15)
    The interval, in seconds, at which the script polls the API (mind the rate limit!)


  skip_first_poll (False, any, True)
    Whether to skip returning items on the first poll









Examples
--------

.. code-block:: yaml+jinja

    
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





Status
------





Authors
~~~~~~~

- Colin McNaughton (@cloin)

