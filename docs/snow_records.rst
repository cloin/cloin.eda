.. _snow_records_module:


snow_records -- event-driven-ansible source plugin for ServiceNow records
=========================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Poll ServiceNow API for new records in a table

Only retrieves records created after the script began executing

This script can be tested outside of ansible-rulebook by specifying environment variables for SN_HOST, SN_USERNAME, SN_PASSWORD, SN_TABLE






Parameters
----------

  instance (True, any, None)
    URL of ServiceNow instance


  username (True, any, None)
    Basic auth username


  password (True, any, None)
    Basic auth password


  table (True, any, None)
    ServiceNow table to watch for new records created


  query (False, any, sys_created_onONToday@javascript:gs.beginningOfToday()@javascript:gs.endOfToday())
    Records to query


  interval (False, any, 5)
    Seconds to wait before performing another query





Notes
-----

.. note::
   - This is currently only capable of basic authentication and is used so far only for demo purposes




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Watch for new records
        hosts: localhost
        sources:
        - cloin.eda.snow_records:
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





Status
------





Authors
~~~~~~~

- Colin McNaughton (@cloin)

