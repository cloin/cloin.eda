
### Plugin:
new_records.py

### Purpose:
event-driven-ansible source plugin example

### Description:
Poll ServiceNow API for new records in a table
Only retrieves records created after the script began executing
This script can be tested outside of ansible-rulebook by specifying
environment variables for SN_HOST, SN_USERNAME, SN_PASSWORD, SN_TABLE

### Arguments:
| Argument | Description |
| --- | --- |
| instance | ServiceNow instance (e.g. https://dev-012345.service-now.com) |
| username | ServiceNow username |
| password | ServiceNow password |
| table | Table to watch for new records |
| query | (optional) Records to query. Defaults to records created today |
| interval | (optional) How often to poll for new records. Defaults to 5 seconds |

### Example(s):
```yaml
- name: Watch for new records
    hosts: localhost
    sources:
    - cloin.servicenow.new_records:
        instance: https://dev-012345.service-now.com
        username: ansible
        password: ansible
        table: incident
        interval: 1
    rules:
    - name: New record created
        condition: event.sys_id is defined
        action:
        debug:

