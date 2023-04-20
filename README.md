# Event-Driven Ansible - cloin.eda

Event-Driven Ansible content

## Included Content

The following set of content is included within this collection:

### Event Sources 

| Name  | Description |
| ----- | ----------- |
| cloin.eda.elastic | Use the output of Elastic query as event source |

## Usage

The following is an example of how to use the elastic source plugin within an Ansible Rulebook:

```yaml
- name: Elastic events
  hosts: localhost
  sources:
    - cloin.eda.elastic:
        elastic_host: elasticsearch
        elastic_port: 9200
        elastic_username: elastic
        elastic_password: elastic
        elastic_index_pattern: filebeat-*
        query: |
          term:
            container.name.keyword: nginx
        interval: 5

  rules:
    - name: Debug event
      condition: event.ecs is defined and event.nginx.log_level == "error"
      action:
        debug:                     
```

## License

Apache 2.0