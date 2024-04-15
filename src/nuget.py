import os
import re
from .utils import is_version_higher_than, write_unix

def merge_nuget_packages_config(source_path, target_path):
    with open(target_path, 'r') as target_file:
        target_content = target_file.read()

    with open(source_path, 'r') as source_file:
        source_content = source_file.read()

    target_packages = dict(re.findall(r'<package id="([^"]+)" version="([^"]+)"', target_content))
    source_packages = dict(re.findall(r'<package id="([^"]+)" version="([^"]+)"', source_content))

    target_keys = set(target_packages.keys())
    for key in target_keys:
        if key in source_packages and is_version_higher_than(source_packages[key], target_packages[key]):
            target_packages[key] = source_packages[key]

    # replace versions in target
    for key, version in target_packages.items():
        target_content = re.sub(
            fr'<package id="{key}" version="[^"]+"',
            f'<package id="{key}" version="{version}"',
            target_content
        )

    return (target_content, target_packages)


def update_omnisharp_json(json_path, versions):
    with open(json_path, 'r') as json_file:
        json_content = json_file.read()

    for key, version in versions.items():
        json_content = re.sub(
            fr'{key}.[^/]+',
            f'{key}.{version}',
            json_content
        )

    return json_content
