"""
json_flatten_filter.py:   An Ansible filter that flattens keys in JSON objects.

This is useful to flatten information from JSON objects.

Arguments:
    * object_paths = a list of jsonpath strings to be extracted and flattened
"""

import fnmatch
import json
from jsonpath_ng import jsonpath, parse


def matches_object_paths(object_paths, s):
    for pattern in object_paths:
        if fnmatch.fnmatch(s, pattern):
            return True
    return False


def flatten_json(json_data):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(json_data)
    return out


def main(event, object_paths=None):
    if object_paths is None:
        object_paths = []

    q = []
    q.append(event)
    while q:
        o = q.pop()
        if isinstance(o, dict):
            for i in list(o.keys()):
                if matches_object_paths(object_paths, i):
                    flattened = flatten_json(o[i])
                    for k, v in flattened.items():
                        o[i + '_' + k] = v
                else:
                    q.append(o[i])

    return event
