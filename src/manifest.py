import json
import os
import re
from .utils import is_version_higher_than, write_unix

DEPENDENCIES_2D_ONLY = set([
    'com.unity.feature.2d',
    'com.unity.cinemachine',
])

IDENTIFIER_2D_DEPENDENCIES = set([
    'com.unity.feature.2d',
    'com.unity.2d.animation',
    'com.unity.2d.pixel-perfect',
    'com.unity.2d.sprite',
    'com.unity.2d.spriteshape',
    'com.unity.2d.tilemap',
    'com.unity.2d.tilemap.extras',
])

DEPENDENCIES_3D_ONLY = set([
    'com.unity.feature.characters-animation',
    'com.unity.feature.worldbuilding',
    'com.unity.progrids',
    'com.unity.ai.navigation',
])

DEPENDENCIES_MOBILE_ONLY = set([
    'com.unity.feature.mobile',
    'com.unity.services.levelplay',
    'com.unity.purchasing',
])

IDENTIFIER_MOBILE_DEPENDENCIES = DEPENDENCIES_MOBILE_ONLY.union(set([
    'com.unity.mobile.android-logcat',
    'com.unity.adaptiveperformance',
    'com.unity.mobile.notifications',
]))

REMOVE_ON_MINIMAL = set([
    'com.unity.collections',
    'com.unity.localization',
    'com.unity.recorder',
    'com.unity.test-framework',
    'com.unity.services.analytics',
    'com.unity.timeline',
    'com.unity.visualscripting',
    'com.unity.collab-proxy',
    'com.unity.ide.rider',
    'com.unity.addressables',
    'com.unity.memoryprofiler',
])

ALWAYS_REMOVE = [
    'com.unity.ide.vscode',
]

def merge_manifests(target_path, source_path, add_new_dependencies=True, filters={}):
    with open(target_path, 'r') as manifest_file:
        target_manifest_str = manifest_file.read()

    with open(source_path, 'r') as manifest_file:
        source_json = json.load(manifest_file)

    target_json = json.loads(target_manifest_str)
    target_dependencies = target_json['dependencies']
    source_dependencies = source_json['dependencies']
    dependencies_to_remove = __dependencies_to_remove(filters)

    # update versions in target
    version_updates = []
    intersection_keys = target_dependencies.keys() & source_dependencies.keys()
    for key in intersection_keys:
        is_source_higher = is_version_higher_than(source_dependencies[key], target_dependencies[key])
        # print(f'[comparing-{key}] source:{source_dependencies[key]} target:{target_dependencies[key]} is-source-higher:{is_source_higher}')
        if is_source_higher:
            version_updates.append(f"{key}: {target_dependencies[key]} -> {source_dependencies[key]}")
            target_dependencies[key] = source_dependencies[key]

    for (key, version) in target_dependencies.items():
        dependency_pattern = r'"' + re.escape(key) + r'"\s*:\s*"[^"]+"'
        target_manifest_str = re.sub(dependency_pattern, f'"{key}": "{version}"', target_manifest_str)

    removed_dependencies = []
    for key in dependencies_to_remove:
        dependency_pattern = r'[^\n]*"' + re.escape(key) + r'"[^\n]*\n'
        if re.search(dependency_pattern, target_manifest_str):
            removed_dependencies.append(key)
        target_manifest_str = re.sub(dependency_pattern, '', target_manifest_str)

    # generates new dependency lines
    only_in_source = source_dependencies.keys() - target_dependencies.keys()
    only_in_source -= dependencies_to_remove
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

    return {
        'new_manifest': target_manifest_str,
        'new_dependencies_snippet': new_dependencies_lines,
        'version_updates_snippet': version_updates_lines,
        'removed_dependencies': removed_dependencies,
    }

def is_2d_manifest(manifest_path):
    with open(manifest_path, 'r') as manifest_file:
        manifest_content = manifest_file.read()

    return any([dep in manifest_content for dep in IDENTIFIER_2D_DEPENDENCIES])

def is_mobile_manifest(manifest_path):
    with open(manifest_path, 'r') as manifest_file:
        manifest_content = manifest_file.read()

    return any([dep in manifest_content for dep in IDENTIFIER_MOBILE_DEPENDENCIES])

def __dependencies_to_remove(filters = {}):
    is_2d = filters.get('2d', False)
    is_3d = filters.get('3d', False)
    is_minimal = filters.get('minimal', False)
    is_mobile = filters.get('mobile', False)
    if not is_2d and not is_3d:
        is_3d = True

    if is_2d and is_3d:
        raise Exception('Cannot have both 2d and 3d filters')

    to_remove = []
    if is_2d:
        to_remove += DEPENDENCIES_3D_ONLY
    else:
        to_remove += DEPENDENCIES_2D_ONLY

    if is_minimal:
        to_remove += REMOVE_ON_MINIMAL
    if not is_mobile:
        to_remove += DEPENDENCIES_MOBILE_ONLY

    to_remove += ALWAYS_REMOVE

    return set(to_remove)
