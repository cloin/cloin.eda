"""alertmanager_filter.py: A filter plugin to extract alert data and host information.

Arguments:
---------
    * data_alerts_path: The JSON path to find alert data. Defaults to "alerts".
      Use empty string "" to treat the whole payload as one alert.
    * data_host_path: The JSON path inside the alert data to find alerting host.
      Defaults to "labels.instance". Use empty string "" if no host information is needed.
    * data_path_separator: The separator to interpret data_alerts_path and data_host_path.
      Defaults to ".".

Example:
-------
    - ansible.eda.alertmanager_filter:
        data_alerts_path: alerts
        data_host_path: labels.instance
        data_path_separator: .
"""

from __future__ import annotations

from typing import Any, Optional
from dpath import util
import logging

LOGGER = logging.getLogger(__name__)

def main(
    event: dict[str, Any],
    data_alerts_path: str = "alerts",
    data_host_path: str = "labels.instance",
    data_path_separator: str = ".",
) -> dict[str, Any]:
    """Extract alert data and host information from an event."""
    alerts = []
    # If data_alerts_path is empty, treat the entire event as a single alert.
    if not data_alerts_path:
        alerts = [event]
    else:
        try:
            # Extract alerts from the event using the specified JSON path.
            alerts = util.get(event, data_alerts_path, separator=data_path_separator)
            # Ensure alerts is a list, even if only one alert is found.
            if not isinstance(alerts, list):
                alerts = [alerts]
        except KeyError:
            # Log an error if the specified path does not exist in the event.
            LOGGER.error(f"Event {event} does not contain path {data_alerts_path}")
            return event

    all_hosts = []
    for alert in alerts:
        hosts = []
        if data_host_path:
            try:
                # Extract the host information from the alert using the specified JSON path.
                host = util.get(alert, data_host_path, separator=data_path_separator)
                # Clean the host value (e.g., remove port if present).
                host = clean_host(host)
                if host is not None:
                    hosts.append(host)
            except KeyError:
                # Log an error if the specified host path does not exist in the alert.
                LOGGER.error(f"Alert {alert} does not contain path {data_host_path}")

        # Add the extracted hosts to the list of all hosts.
        all_hosts.extend(hosts)

    # Ensure the event has a "meta" key and add the extracted hosts under "meta".
    if "meta" not in event:
        event["meta"] = {}
    event["meta"]["hosts"] = all_hosts

    return event

def clean_host(host: str) -> str:
    """Remove port from host string if it exists."""
    # Split the host string by ':' and return only the hostname part (without the port).
    if ":" in host:
        return host.split(":")[0]
    return host
