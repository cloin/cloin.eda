.. _nextdns_module:


nextdns -- An ansible-rulebook event source plugin for NextDNS logs
===================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Uses the NextDNS API to subscribe to a SSE event stream for the logs of a specific profile and use these as events in Event-Driven Ansible






Parameters
----------

  api_key (True, any, None)
    Your NextDNS API key


  profile_id (True, any, None)
    Your NextDNS profile ID









Examples
--------

.. code-block:: yaml+jinja

    
    - name: NextDNS event stream
        hosts: localhost
        sources:
        - cloin.eda.nextdns:
            profile_id: ""
            api_key: ""





Status
------





Authors
~~~~~~~

- Colin McNaughton (@cloin)

