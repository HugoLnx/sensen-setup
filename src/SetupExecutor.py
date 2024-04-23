import os
import glob
from datetime import datetime
import shutil
import subprocess
from src.manifest import merge_manifests
from src.utils import write_unix, to_unixpath

SETUP_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
PROJECT_ROOT = os.path.abspath(os.path.join(SETUP_ROOT, '..'))
BKP_FOLDER = os.path.join(SETUP_ROOT, 'bkp')
SUBMODULES_FOLDER = os.path.join(PROJECT_ROOT, 'Assets', 'Plugins', 'Submodules')
DEFAULT_PROJECT_NAME = os.path.basename(PROJECT_ROOT)

MANIFEST_PROJECT_PATH = os.path.join(PROJECT_ROOT, 'Packages', 'manifest.json')
MANIFEST_SETUP_PATH = os.path.join(SETUP_ROOT, 'ConfigFiles', 'manifest.json')

class SetupExecutor:
    def __init__(self, project_name, manifest_filters):
        self.project_name = project_name or DEFAULT_PROJECT_NAME
        self.manifest_filters = manifest_filters

    def backup_config_files(self):
        os.makedirs(BKP_FOLDER, exist_ok=True)
        self.__backup_file_if_exists('.gitignore')
        self.__backup_file_if_exists('.gitattributes')
        self.__backup_file_if_exists('.editorconfig')
        self.__backup_file_if_exists('manifest.json', 'Packages')

    def init_git(self):
        self.__replace_config('.gitignore', './')
        self.__replace_config('gitattributes', './.gitattributes')
        subprocess.run(['git', 'init'], cwd=PROJECT_ROOT)
        subprocess.run(['git', 'lfs', 'install'], cwd=PROJECT_ROOT)

    def import_configs(self):
        self.__replace_config('.editorconfig', '.')
        self.__copy_all_files('PackagesBatch/*.unitypackage', './PackagesBatch/')

    def create_project_structure(self):
        project_structure_path = os.path.join(PROJECT_ROOT, 'Assets', self.project_name)
        if os.path.exists(project_structure_path):
            print(f'!!! Project structure folder already exists: {project_structure_path}')
        else:
            shutil.copytree(os.path.join(SETUP_ROOT, 'Templates/ProjectStructure/'), project_structure_path)
        self.__ensure_folder('Assets/Vendor')
        self.__ensure_folder('Assets/Plugins/_Ignore')
        scripts_folder = os.path.join(project_structure_path, 'Code', 'Scripts')
        self.__ensure_assembly_definition_on(scripts_folder)

    def add_submodules(self, only_toolkit=False):
        os.makedirs(SUBMODULES_FOLDER, exist_ok=True)
        subprocess.run(['git', 'submodule', 'init'], cwd=PROJECT_ROOT)
        self.__add_submodule('dev', 'https://github.com/HugoLnx/unity-lnx-arch.git', 'unity-lnx-arch')
        self.__add_submodule('dev', 'https://github.com/HugoLnx/unity-sensen-components.git', 'unity-sensen-components')
        self.__add_submodule('dev', 'https://github.com/HugoLnx/unity-sensen-toolkit.git', 'unity-sensen-toolkit')
        subprocess.run(['git', 'submodule', 'update', '--recursive', '--remote'], cwd=PROJECT_ROOT)

    def del_submodules(self, only_toolkit=False):
        subprocess.run(['git', 'submodule', 'deinit', '--force', '--all'], cwd=PROJECT_ROOT)
        self.__del_submodule('unity-lnx-arch')
        self.__del_submodule('unity-sensen-components')
        self.__del_submodule('unity-sensen-toolkit')

        shutil.rmtree(SUBMODULES_FOLDER, ignore_errors=True)
        print(f"Deleted folder {SUBMODULES_FOLDER}")

        gitmodules_path = os.path.join(PROJECT_ROOT, '.gitmodules')
        if os.path.exists(gitmodules_path):
            os.remove(gitmodules_path)
        print(f"Deleted file {gitmodules_path}")

    def cleanup_submodules(self):
        subprocess.run(['git', 'submodule', 'deinit', '-f', '.'], cwd=PROJECT_ROOT)
        shutil.rmtree(SUBMODULES_FOLDER, ignore_errors=True)

    def pull_manifest(self):
        result = merge_manifests(
            source_path=MANIFEST_PROJECT_PATH,
            target_path=MANIFEST_SETUP_PATH,
            add_new_dependencies=False
        )
        new_manifest = result['new_manifest']
        new_dependencies_snippet = result['new_dependencies_snippet']
        version_updates_snippet = result['version_updates_snippet']

        if version_updates_snippet is not None:
            write_unix(MANIFEST_SETUP_PATH, new_manifest)
            print('Updated setup base manifest...')
            print(version_updates_snippet)
        else:
            print('Setup manifest has no versions to update')

        if new_dependencies_snippet is not None:
            print('> Project manifest has dependencies that are not in source manifest...')
            print(new_dependencies_snippet)
            print('Consider adding them manually to the setup manifest')

    def push_manifest(self):
        result = merge_manifests(
            source_path=MANIFEST_SETUP_PATH,
            target_path=MANIFEST_PROJECT_PATH,
            add_new_dependencies=True,
            filters=self.manifest_filters
        )
        new_manifest = result['new_manifest']
        new_dependencies_snippet = result['new_dependencies_snippet']
        version_updates_snippet = result['version_updates_snippet']
        removed_dependencies = result['removed_dependencies']

        has_updates = version_updates_snippet is not None \
            or new_dependencies_snippet is not None \
            or len(removed_dependencies) > 0

        if has_updates:
            write_unix(MANIFEST_PROJECT_PATH, new_manifest)
            print('> Updated project manifest...')
            print(version_updates_snippet)
        else:
            print('Project manifest is already up-to-date')

        if new_dependencies_snippet is not None:
            print('> Added new dependencies to project manifest')
            print(new_dependencies_snippet)

        if len(removed_dependencies) > 0:
            print('> Removed dependencies from project manifest')
            print('\n'.join(removed_dependencies))

    def __add_submodule(self, branch_name, git_url, folder_name):
        folder_path = os.path.join(SUBMODULES_FOLDER, folder_name)
        folder_relpath = to_unixpath(os.path.relpath(folder_path, PROJECT_ROOT))
        cmd = ['git', 'submodule', 'add', '-f', '-b', branch_name, '--', git_url, folder_relpath]
        subprocess.run(cmd, cwd=PROJECT_ROOT)

    def __del_submodule(self, folder_name):
        folder_path = os.path.join(SUBMODULES_FOLDER, folder_name)
        folder_relpath = to_unixpath(os.path.relpath(folder_path, PROJECT_ROOT))
        cmd = ['git', 'rm', '-f', folder_relpath]
        subprocess.run(cmd, cwd=PROJECT_ROOT)

    def __replace_config(self, config_relative_path, target_relative_path):
        config_path = os.path.join(SETUP_ROOT, 'ConfigFiles', config_relative_path)
        target_path = os.path.join(PROJECT_ROOT, target_relative_path)
        shutil.copy(config_path, target_path)

    def __copy_all_files(self, source_folder, target_folder):
        source_path = os.path.join(SETUP_ROOT, source_folder)
        target_path = os.path.abspath(os.path.join(PROJECT_ROOT, target_folder))
        os.makedirs(target_path, exist_ok=True)

        source_files = glob.glob(source_path)
        for source_file in source_files:
            if os.path.isfile(source_file):
                shutil.copy(source_file, target_path)
                print(f'Copied {source_file} to {target_path}')

    def __ensure_folder(self, folder_relative_path):
        folder_path = os.path.join(PROJECT_ROOT, folder_relative_path)
        os.makedirs(folder_path, exist_ok=True)
        open(os.path.join(folder_path, '.gitkeep'), 'a').close()

    def __ensure_assembly_definition_on(self, folder_path):
        template_path = os.path.join(SETUP_ROOT, 'ConfigFiles', 'AssemblyDefinition.asmdef')
        with open(template_path, 'r') as template_file:
            template_content = template_file.read()
        assembly_definition_content = template_content.replace('<PROJECT_NAME>', self.project_name) 

        assembly_definition_path = os.path.join(folder_path, f"{self.project_name}.asmdef")
        write_unix(assembly_definition_path, assembly_definition_content)

    def __backup_file_if_exists(self, filename, filefolder='.'):
        filepath = os.path.join(filefolder, filename)
        if os.path.isfile(filepath):
            print(f'Backing up {filename} in bkp/')
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            shutil.copy(filepath, os.path.join(BKP_FOLDER, f'{timestamp}_{filename}'))
