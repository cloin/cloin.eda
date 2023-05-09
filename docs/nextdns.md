
### Plugin:
nextdns.py

### Purpose
An ansible-rulebook event source plugin for NextDNS logs.

### Arguments:
| Argument | Description |
| --- | --- |
| api_key | Your NextDNS API key |
| profile_id | Your NextDNS profile ID |

### Examples:
- name: NextDNS event stream
    hosts: localhost
    sources:
        - nextdns:
            profile_id: ""
            api_key: ""

