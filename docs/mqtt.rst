.. _mqtt_module:


mqtt -- event-driven-ansible source plugin for mqtt
===================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Subscribes topic on mqtt and prints messages to ansible-rulebook

Test script stand-alone by exporting MQTT_HOST and MQTT_TOPIC as environment variables MQTT_HOST, MQTT_TOPIC






Parameters
----------

  host (True, any, None)
    URL for mqtt broker


  topic (True, any, None)
    Topic to subscribe to for events





Notes
-----

.. note::
   - This is currently only capable of basic authentication and is used so far only for demo purposes




Examples
--------

.. code-block:: yaml+jinja

    
        - name: Minecraft events
          hosts: localhost
          sources:
            - cloin.eda.mqtt:
                host: localhost
                topic: messages

          rules:
            - name: New minecraft event
              condition: event.type is defined
              action:
                debug:





Status
------





Authors
~~~~~~~

- Colin McNaughton (@cloin)

