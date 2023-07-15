import requests
import logging

def main(event: dict, webhook_url: str = None) -> dict:
    """
    Perform an HTTP POST request to the specified webhook receiver URL with the 
    event dictionary as the JSON body, log the response, and return the event.
    The dictionary is only sent if the webhook_url is provided.

    THIS IS ONLY MEANT TO ASSIST IN DEV. I use this to better understand the
    event structure so that I can write rule conditions easier
    
    Parameters
    ----------
    event : dict
        The dictionary to be sent as the JSON body of the POST request.
    webhook_url : str, optional
        The URL of the webhook receiver. If not provided, the event is not sent
        and is simply returned.
    
    Returns
    -------
    dict
        The original event dictionary.

    Rulebook example
    ----------------

   - name: Respond to webhook POST
     hosts: localhost
     sources:
       - ansible.eda.webhook:
           host: 0.0.0.0
           port: 5000
         filters:
           - cloin.eda.poster:
               webhook_url: https://webhook.site/asdfa2q3423-sadf-449231-asd-88f81e0asdf65d33
            
    """
    if not webhook_url:
        logging.info("Webhook URL not defined. The event dictionary will not be sent.")
        return event

    try:
        logging.info("POSTing event dictionary")
        response = requests.post(webhook_url, json=event)
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        logging.error(f"An HTTP error occurred: {e}")
        if response:
            logging.error(f"Response Text: {response.text}")
        return event

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return event

    else:
        logging.info(f"Response Status Code: {response.status_code}")

    return event
