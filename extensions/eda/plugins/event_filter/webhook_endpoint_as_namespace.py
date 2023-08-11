import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main(event: dict) -> dict:
    """
    Take the value of event['meta']['endpoint'] and create a new namespace for the event.
    Both the event payload and all the meta information will be moved under this new namespace if the endpoint is specified.

    For example:
    If the event is received on the "testing" endpoint, everything including 
    the event payload and all meta information should be accessible under event['testing'].

    If the endpoint isn't specified, it returns the original event.

    Parameters
    ----------
    event : dict
        The dictionary containing the event data.

    Returns
    -------
    dict
        The modified event dictionary with the new namespace based on the endpoint, or the original event if no endpoint is specified.
    """
    try:
        logger.debug("Starting filter process...")

        # Extract endpoint from the event meta
        endpoint = event['meta'].get('endpoint')
        
        if not endpoint:
            logger.warning("Endpoint not found. Returning the original event.")
            return event

        logger.debug(f"Extracted endpoint: {endpoint}")

        # Create a new namespace using the endpoint and move both the payload and 
        # all meta information to this new namespace
        event = {
            endpoint: event
        }

        logger.debug(f"Modified event: {event}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return event
    
    return event
