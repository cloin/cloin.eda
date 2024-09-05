import paho.mqtt.client as mqtt
import logging

def main(event: dict, mqtt_broker: str = None, mqtt_topic: str = None, mqtt_port: int = 1883) -> dict:
    """
    Publish an event dictionary as an MQTT message to a specified topic on an MQTT broker.
    If mqtt_topic is not provided, use 'meta.endpoint' from the event as the topic.
    If 'meta.endpoint' is null or missing, default to 'ansible'. 
    After the message is sent, update the 'meta' key with the success or failure status.
    
    Parameters
    ----------
    event : dict
        The dictionary to be sent as the MQTT message payload.
    mqtt_broker : str, optional
        The address of the MQTT broker.
    mqtt_topic : str, optional
        The MQTT topic to publish the event to. Defaults to 'ansible'. If not provided, 
        the value of event['meta']['endpoint'] is used if available.
    mqtt_port : int, optional
        The port on which the MQTT broker is running (default is 1883).
    
    Returns
    -------
    dict
        The original event dictionary, with an updated 'meta' key that contains the 
        success or failure of the MQTT message operation.

    """
    if not mqtt_broker:
        logging.error("MQTT broker is not defined.")
        return event

    # Ensure meta exists in the event dictionary
    if 'meta' not in event:
        event['meta'] = {}

    # If mqtt_topic is not provided, check if meta.endpoint exists and is not null or empty
    if not mqtt_topic:
        mqtt_topic = event.get('meta', {}).get('endpoint')
        if not mqtt_topic:  # Handle null, missing, or empty endpoint
            mqtt_topic = 'ansible'

    try:
        # Create MQTT client
        client = mqtt.Client()

        # Connect to the broker
        logging.info(f"Connecting to MQTT broker at {mqtt_broker}:{mqtt_port}")
        client.connect(mqtt_broker, mqtt_port)

        # Publish the event as a message to the dynamically determined topic
        logging.info(f"Publishing event to topic {mqtt_topic}")
        client.publish(mqtt_topic, str(event))

        # Disconnect after publishing
        client.disconnect()

        # Update meta with success status
        event['meta']['mqtt_status'] = 'success'

    except Exception as e:
        logging.error(f"An error occurred while sending the MQTT message: {e}")
        
        # Update meta with failure status and error message
        event['meta']['mqtt_status'] = 'failure'
        event['meta']['error_message'] = str(e)

    return event