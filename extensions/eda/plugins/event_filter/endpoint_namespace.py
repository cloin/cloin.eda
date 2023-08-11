def namespace_event_by_endpoint(event: dict) -> dict:
    """
    Take the value of event['meta']['endpoint'] and create a new namespace for the event.
    The event payload and meta information will be moved under this new namespace.

    For example:
    If the event is received on the "testing" endpoint, the event payload and meta 
    information should be accessible under event['testing']['payload'] and 
    event['testing']['meta'], respectively.

    Parameters
    ----------
    event : dict
        The dictionary containing the event data.

    Returns
    -------
    dict
        The modified event dictionary with the new namespace based on the endpoint.
    """
    
    # Extract endpoint from the event meta
    endpoint = event['meta']['endpoint']
    
    # Create a new namespace using the endpoint and move the payload and meta information 
    # to this new namespace
    event[endpoint] = {
        'payload': event.pop('payload'),
        'meta': event.pop('meta')
    }
    
    return event
