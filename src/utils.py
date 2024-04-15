import re
import os

def is_version_higher_than(version1, version2):
    v1_parts = [int(x) for x in re.findall(r'\d+', version1)]
    v2_parts = [int(x) for x in re.findall(r'\d+', version2)]

    length = min(len(v1_parts), len(v2_parts))

    for i in range(length):
        if len(v1_parts) <= i or len(v2_parts) <= i:
            return False
        elif v1_parts[i] > v2_parts[i]:
            return True
        elif v1_parts[i] < v2_parts[i]:
            return False

    return False

def write_unix(config_path, content):
    with open(config_path, 'w', newline='\n') as config_file:
        config_file.write(content)
