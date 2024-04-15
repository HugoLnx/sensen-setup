import json
import os
import re

def write_manifest(manifest_path, content):
    with open(manifest_path, 'w', newline='\n') as manifest_file:
        manifest_file.write(content)

def merge_manifests(target_path, source_path, add_new_dependencies=True):
    with open(target_path, 'r') as manifest_file:
        target_manifest_str = manifest_file.read()

    with open(source_path, 'r') as manifest_file:
        source_json = json.load(manifest_file)

    target_json = json.loads(target_manifest_str)
    target_dependencies = target_json['dependencies']
    source_dependencies = source_json['dependencies']

    # update versions in target
    version_updates = []
    intersection_keys = target_dependencies.keys() & source_dependencies.keys()
    for key in intersection_keys:
        is_source_higher = __is_version_higher_than(source_dependencies[key], target_dependencies[key])
        # print(f'[comparing-{key}] source:{source_dependencies[key]} target:{target_dependencies[key]} is-source-higher:{is_source_higher}')
        if is_source_higher:
            version_updates.append(f"{key}: {target_dependencies[key]} -> {source_dependencies[key]}")
            target_dependencies[key] = source_dependencies[key]

    for (key, version) in target_dependencies.items():
        dependency_pattern = r'"' + re.escape(key) + r'"\s*:\s*"[^"]+"'
        target_manifest_str = re.sub(dependency_pattern, f'"{key}": "{version}"', target_manifest_str)

    # generates new dependency lines
    only_in_source = source_dependencies.keys() - target_dependencies.keys()
    if len(only_in_source) == 0:
        new_dependencies_lines = None
    else:
        dependency_line_pattern = r'"dependencies"\s*:.*(\n\s*"[^"]+"\s*:\s*"[^"]+"[^\n]+)'
        dependency_line_match = re.search(dependency_line_pattern, target_manifest_str)[1]
        new_dependencies_lines = ""
        for key in only_in_source:
            new_dependencies_lines += re.sub(r'".*:.*".*"', f'"{key}": "{source_dependencies[key]}"', dependency_line_match)

        if add_new_dependencies:
            target_manifest_str = re.sub(r'("dependencies".*:[^\n]+)', f"\\1{new_dependencies_lines}", target_manifest_str)

    version_updates_lines = '\n'.join(version_updates) if len(version_updates) > 0 else None
    return (target_manifest_str, new_dependencies_lines, version_updates_lines)

def __is_version_higher_than(version1, version2):
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
