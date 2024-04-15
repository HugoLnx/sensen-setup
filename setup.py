#!/usr/bin/env python3
import os
import glob
from datetime import datetime
import argparse
import shutil
import subprocess
from src.manifest import merge_manifests
from src.nuget import merge_nuget_packages_config, update_omnisharp_json
from src.utils import write_unix

SETUP_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SETUP_ROOT, '..'))
BKP_FOLDER = os.path.join(SETUP_ROOT, 'bkp')
SUBMODULES_FOLDER = os.path.join(PROJECT_ROOT, 'Assets', 'Plugins', 'Submodules')
DEFAULT_PROJECT_NAME = os.path.basename(PROJECT_ROOT)

OMNISHARP_SETUP_PATH = os.path.join(SETUP_ROOT, 'ConfigFiles', 'omnisharp.json')

MANIFEST_PROJECT_PATH = os.path.join(PROJECT_ROOT, 'Packages', 'manifest.json')
MANIFEST_SETUP_PATH = os.path.join(SETUP_ROOT, 'ConfigFiles', 'manifest.json')
NUGET_PROJECT_PATH = os.path.join(PROJECT_ROOT, 'Assets', 'packages.config')
NUGET_SETUP_PATH = os.path.join(SETUP_ROOT, 'ConfigFiles', 'packages.config')

COMMAND_INIT_GIT = 'init-git'
COMMAND_SETUP_INIT = 'init'
COMMAND_SETUP_ALL = 'all'
COMMAND_INIT_SUBMODULES = 'init-submodules'
COMMAND_RM_SUBMODULES = 'rm-submodules'
COMMAND_PULL_MANIFEST = 'pull-manifest'
COMMAND_PUSH_MANIFEST = 'push-manifest'
COMMAND_PULL_NUGET = 'pull-nuget'
COMMAND_PUSH_NUGET = 'push-nuget'
COMMANDS = [
    COMMAND_INIT_GIT,
    COMMAND_SETUP_INIT,
    COMMAND_SETUP_ALL,
    COMMAND_INIT_SUBMODULES,
    COMMAND_RM_SUBMODULES,
    COMMAND_PULL_MANIFEST,
    COMMAND_PUSH_MANIFEST,
    COMMAND_PULL_NUGET,
    COMMAND_PUSH_NUGET,
]

# BACKUP CONFIG FILES
def backup_file_if_exists(filename, filefolder='.'):
    filepath = os.path.join(filefolder, filename)
    if os.path.isfile(filepath):
        print(f'Backing up {filename} in bkp/')
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        shutil.copy(filepath, os.path.join(BKP_FOLDER, f'{timestamp}_{filename}'))

def backup_config_files():
    backup_file_if_exists('.gitignore')
    backup_file_if_exists('.gitattributes')
    backup_file_if_exists('.editorconfig')
    backup_file_if_exists('omnisharp.json')
    backup_file_if_exists('NuGet.config', 'Assets')
    backup_file_if_exists('packages.config', 'Assets')
    backup_file_if_exists('manifest.json', 'Packages')

def init_git():
    __replace_config('.gitignore', './')
    __replace_config('gitattributes', './.gitattributes')
    subprocess.run(['git', 'init'], cwd=PROJECT_ROOT)
    subprocess.run(['git', 'lfs', 'install'], cwd=PROJECT_ROOT)

def import_configs():
    push_manifest()
    push_nuget()
    __replace_config('.editorconfig', '.')
    __copy_all_files('PackagesBatch/*.unitypackage', './PackagesBatch/')

def create_project_structure():
    project_structure_path = os.path.join(PROJECT_ROOT, 'Assets', args.name)
    if os.path.exists(project_structure_path):
        print(f'!!! Project structure folder already exists: {project_structure_path}')
    else:
        shutil.copytree(os.path.join(SETUP_ROOT, 'Templates/ProjectStructure/'), project_structure_path)
    __ensure_folder('Assets/Vendor')
    __ensure_folder('Assets/Plugins/_Ignore')

def init_submodules(only_toolkit=False):
    os.makedirs(SUBMODULES_FOLDER, exist_ok=True)
    subprocess.run(['git', 'submodule', 'init'], cwd=PROJECT_ROOT)
    if not only_toolkit:
        __add_submodule('dev', 'https://github.com/HugoLnx/unity-lnx-arch.git', 'unity-lnx-arch')
        __add_submodule('dev', 'https://github.com/HugoLnx/unity-sensen-components.git', 'unity-sensen-components')
    __add_submodule('dev', 'https://github.com/HugoLnx/unity-sensen-toolkit.git', 'unity-sensen-toolkit')
    subprocess.run(['git', 'submodule', 'update', '--recursive', '--remote'], cwd=PROJECT_ROOT)

def cleanup_submodules():
    subprocess.run(['git', 'submodule', 'deinit', '-f', '.'], cwd=PROJECT_ROOT)
    shutil.rmtree(SUBMODULES_FOLDER, ignore_errors=True)

def pull_manifest():
    (new_manifest, new_dependencies_snippet, version_updates_snippet) = merge_manifests(
        source_path=MANIFEST_PROJECT_PATH,
        target_path=MANIFEST_SETUP_PATH,
        add_new_dependencies=False
    )

    if version_updates_snippet is not None:
        write_unix(MANIFEST_SETUP_PATH, new_manifest)
        print('Updated setup base manifest...')
        print(version_updates_snippet)
    else:
        print('Setup manifest has no versions to update')

    if new_dependencies_snippet is not None:
        print('Project manifest has dependencies that are not in source manifest...')
        print(new_dependencies_snippet)
        print('Consider adding them manually to the setup manifest')

def push_manifest():
    (new_manifest, new_dependencies_snippet, version_updates_snippet) = merge_manifests(
        source_path=MANIFEST_SETUP_PATH,
        target_path=MANIFEST_PROJECT_PATH,
        add_new_dependencies=True
    )
    has_updates = version_updates_snippet is not None or new_dependencies_snippet is not None

    if has_updates:
        write_unix(MANIFEST_PROJECT_PATH, new_manifest)
        print('Updated project manifest...')
        print(version_updates_snippet)
    else:
        print('Project manifest is already up-to-date')

    if new_dependencies_snippet is not None:
        print('Added new dependencies to project manifest')
        print(new_dependencies_snippet)

def pull_nuget():
    (new_content, packages) = merge_nuget_packages_config(
        source_path=NUGET_PROJECT_PATH,
        target_path=NUGET_SETUP_PATH,
    )

    write_unix(NUGET_SETUP_PATH, new_content)

    new_json_content = update_omnisharp_json(OMNISHARP_SETUP_PATH, packages)
    write_unix(OMNISHARP_SETUP_PATH, new_json_content)

def push_nuget():
    __replace_config('omnisharp.json', '.')
    __replace_config('NuGet.config', 'Assets')
    __replace_config('packages.config', 'Assets')


def __add_submodule(branch_name, git_url, folder_name):
    folder_path = os.path.join(SUBMODULES_FOLDER, folder_name)
    folder_relpath = os.path.relpath(folder_path, PROJECT_ROOT)
    cmd = ['git', 'submodule', 'add', '-f', '-b', branch_name, '--', git_url, folder_relpath]
    subprocess.run(cmd, cwd=PROJECT_ROOT)

def __replace_config(config_relative_path, target_relative_path):
    config_path = os.path.join(SETUP_ROOT, 'ConfigFiles', config_relative_path)
    target_path = os.path.join(PROJECT_ROOT, target_relative_path)
    shutil.copy(config_path, target_path)

def __copy_all_files(source_folder, target_folder):
    source_path = os.path.join(SETUP_ROOT, source_folder)
    target_path = os.path.abspath(os.path.join(PROJECT_ROOT, target_folder))
    os.makedirs(target_path, exist_ok=True)

    source_files = glob.glob(source_path)
    for source_file in source_files:
        if os.path.isfile(source_file):
            shutil.copy(source_file, target_path)
            print(f'Copied {source_file} to {target_path}')

def __ensure_folder(folder_relative_path):
    folder_path = os.path.join(PROJECT_ROOT, folder_relative_path)
    os.makedirs(folder_path, exist_ok=True)
    open(os.path.join(folder_path, '.gitkeep'), 'a').close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=COMMANDS, default=COMMANDS[0], help='Command to run', type=str)
    parser.add_argument('--name', default=DEFAULT_PROJECT_NAME, help='Name of the game', type=str, required=False)
    args = parser.parse_args()

    if args.command not in COMMANDS:
        print(f'Invalid command: {args.command}')
        print(f'Valid commands: {COMMANDS}')
        exit(1)

    if args.command == COMMAND_INIT_GIT:
        backup_config_files()
        init_git()
    elif args.command == COMMAND_SETUP_INIT:
        backup_config_files()
        init_git()
        import_configs()
        init_submodules(only_toolkit=True)
    elif args.command == COMMAND_SETUP_ALL:
        backup_config_files()
        init_git()
        import_configs()
        create_project_structure()
        init_submodules()
    elif args.command == COMMAND_INIT_SUBMODULES:
        init_git()
        init_submodules()
    elif args.command == COMMAND_RM_SUBMODULES:
        cleanup_submodules()
    elif args.command == COMMAND_PULL_MANIFEST:
        pull_manifest()
    elif args.command == COMMAND_PUSH_MANIFEST:
        push_manifest()
    elif args.command == COMMAND_PULL_NUGET:
        pull_nuget()
    elif args.command == COMMAND_PUSH_NUGET:
        push_nuget()
