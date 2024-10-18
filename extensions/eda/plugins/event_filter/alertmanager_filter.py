"""alertmanager_filter.py: A filter plugin to extract alert data and host information.

Arguments:
---------
    * data_alerts_path: The JSON path to find alert data. Defaults to "alerts".
      Use empty string "" to treat the whole payload as one alert.
    * data_host_path: The JSON path inside the alert data to find alerting host.
      Defaults to "labels.instance". Use empty string "" if no host information is needed.
    * data_path_separator: The separator to interpret data_alerts_path and data_host_path.
      Defaults to ".".
    * skip_original_data: true/false. Default to false.
      true: Only alert data will be returned as events.
      false: Both the original event and each parsed alert will be returned as events.

Example:
-------
    - name: Respond to webhook POST
      hosts: localhost
      sources:
        - ansible.eda.webhook:
            host: 0.0.0.0
            port: 5000
          filters:
            - ansible.eda.alertmanager_filter:
                data_alerts_path: alerts
                data_host_path: labels.instance
                data_path_separator: .
                skip_original_data: false
"""

from __future__ import annotations

from typing import Any, Optional, List
from dpath import util
import logging

LOGGER = logging.getLogger(__name__)

def main(
    event: dict[str, Any],
    data_alerts_path: str = "alerts",
    data_host_path: str = "labels.instance",
    data_path_separator: str = ".",
    skip_original_data: bool = False,
) -> List[dict[str, Any]]:
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
        except (KeyError, TypeError):
            # Log an error if the specified path does not exist in the event or if the path is incorrect.
            LOGGER.error(f"Event {event} does not contain path {data_alerts_path}")
            return [event]

    for alert in alerts:
        hosts = []
        if data_host_path:
            try:
                # Extract the host information from the alert using the specified JSON path.
                host = util.get(alert, data_host_path, separator=data_path_separator)
                # Ensure the extracted host is a string or list of strings.
                if isinstance(host, (str, list)):
                    if isinstance(host, str):
                        host = clean_host(host)
                        hosts.append(host)
                    elif isinstance(host, list):
                        hosts.extend([clean_host(h) for h in host if isinstance(h, str)])
            except (KeyError, TypeError):
                # Log an error if the specified host path does not exist in the alert.
                LOGGER.error(f"Alert {alert} does not contain path {data_host_path}")

        # Create a new event for each alert, including the extracted host information.
        new_event = {
            "alert": alert,
            "meta": {
                "hosts": hosts
            }
        }

    print(new_event)

def clean_host(host: str) -> str:
    """Remove port from host string if it exists."""
    # Split the host string by ':' and return only the hostname part (without the port).
    if ":" in host:
        return host.split(":")[0]
    return host
