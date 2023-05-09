
### Plugin:
nextdns.py

### Purpose
An ansible-rulebook event source plugin for NextDNS logs

### Description:
Uses the NextDNS API to subscribe to a SSE event stream
for the logs of a specific profile and use these as events
in Event-Driven Ansible

### Arguments:
| Argument | Description |
| --- | --- |
| api_key | Your NextDNS API key |
| profile_id | Your NextDNS profile ID |

### Examples:
- name: NextDNS event stream
    hosts: localhost
    sources:
        - cloin.eda.nextdns:
            profile_id: ""
            api_key: ""

