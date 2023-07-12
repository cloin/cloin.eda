import requests
import logging

def main(event: dict, webhook_url: str, search: str = None) -> dict:
    """
    Perform an HTTP POST request to the specified webhook receiver URL with the 
    event dictionary as the JSON body, log the response, and return the event.
    The dictionary is only sent if it contains the specified search string or if
    the search string is not provided.

    THIS IS ONLY MEANT TO ASSIST IN DEV. I use this to better understand the
    event structure so that I can write rule conditions easier
    
    Parameters
    ----------
    event : dict
        The dictionary to be sent as the JSON body of the POST request.
    webhook_url : str
        The URL of the webhook receiver.
    search : str, optional
        The string to search for in the dictionary. If not provided, the event
        is sent to the webhook URL regardless.
    
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
           - ansible.eda.normalize_keys:
           - ansible.eda.dashes_to_underscores:
           - cloin.eda.poster:
               webhook_url: https://webhook.site/asdfa2q3423-sadf-449231-asd-88f81e0asdf65d33
               search: "hey"
            
    """
    # Convert the dictionary to a string to search for the substring
    event_str = str(event)

    # If a search string is provided and it's not in the event dictionary, log a warning and return the event
    if search is not None and search not in event_str:
        logging.warning("String not found")
        return event

    try:
        # Send the POST request
        response = requests.post(webhook_url, json=event)
        
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        # If there's an HTTP error, log the exception and the response text (if available)
        logging.error(f"An HTTP error occurred: {e}")
        if response:
            logging.error(f"Response Text: {response.text}")
        return event

    except Exception as e:
        # If there's some other error (like a network error, or a typo in the URL), log the exception
        logging.error(f"An error occurred: {e}")
        return event

    else:
        # If the request was successful, log the status code
        logging.info(f"Response Status Code: {response.status_code}")

    # Return the original event dictionary
    return event
