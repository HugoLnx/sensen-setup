import argparse

from src.SetupExecutor import SetupExecutor, MANIFEST_PROJECT_PATH
from src.manifest import is_2d_manifest, is_mobile_manifest

COMMAND_INIT_GIT = 'git'
COMMAND_INIT_CONFIGS = 'configs'
COMMAND_INIT_STRUCTURE = 'structure'
COMMAND_PULL_MANIFEST = 'pull-manifest'
COMMAND_PUSH_MANIFEST = 'push-manifest'
COMMAND_ADD_SUBMODULES = 'add-submodules'
COMMAND_DEL_SUBMODULES = 'del-submodules'
COMMANDS = [
    COMMAND_INIT_GIT,
    COMMAND_INIT_CONFIGS,
    COMMAND_INIT_STRUCTURE,
    COMMAND_PULL_MANIFEST,
    COMMAND_PUSH_MANIFEST,
    COMMAND_ADD_SUBMODULES,
    COMMAND_DEL_SUBMODULES,
]

if __name__ != '__main__':
    throw('This script should not be imported')

parser = argparse.ArgumentParser()
parser.add_argument('command', choices=COMMANDS, default=COMMANDS[0], help='Command to run', type=str)
parser.add_argument('--name', default=None, help='Name of the game', type=str, required=False)
parser.add_argument('--2d', dest='two_d', default=False, help='Force to use 2D dependencies', action='store_true', required=False)
parser.add_argument('--3d', dest='three_d', default=False, help='Force to use 3D dependencies', action='store_true', required=False)
parser.add_argument('--mobile', default=False, help='Use mobile dependencies', action='store_true', required=False)
parser.add_argument('--desktop', default=False, help='Use desktop dependencies', action='store_true', required=False)
parser.add_argument('--slim', default=False, help='Remove some optional dependencies (good for prototypes and gamejams)', action='store_true', required=False)
args = parser.parse_args()

if args.two_d and args.three_d:
    print('Cannot use 2D and 3D at the same time')
    exit(1)

if args.mobile and args.desktop:
    print('Cannot use mobile and desktop at the same time')
    print('PS.: If you are making a cross-platform game, just use --mobile to add the mobile dependencies')
    exit(1)


is_2d = args.two_d or (not(args.three_d) and is_2d_manifest(MANIFEST_PROJECT_PATH))
is_3d = not is_2d
is_mobile = args.mobile or (not(args.desktop) and is_mobile_manifest(MANIFEST_PROJECT_PATH))
is_slim = args.slim

was_auto_detected = not(args.two_d) and not(args.three_d)
print(f'Using {'2D' if is_2d else '3D'}{' mobile' if is_mobile else ''}{' slim' if is_slim else ''} dependencies {'(Auto-detected)' if was_auto_detected else ''}')

manifest_filters = {
    '2d': is_2d,
    '3d': is_3d,
    'mobile': is_mobile,
    'slim': is_slim,
}

if args.command not in COMMANDS:
    print(f'Invalid command: {args.command}')
    print(f'Valid commands: {COMMANDS}')
    exit(1)

e = SetupExecutor(
    project_name=args.name,
    manifest_filters=manifest_filters,
)

if args.command == COMMAND_INIT_GIT:
    e.backup_config_files()
    e.init_git()
elif args.command == COMMAND_INIT_CONFIGS:
    e.backup_config_files()
    e.push_manifest()
    e.import_configs()
    e.init_submodules(only_toolkit=True)
elif args.command == COMMAND_INIT_STRUCTURE:
    e.create_project_structure()
    e.init_submodules()
elif args.command == COMMAND_PULL_MANIFEST:
    e.pull_manifest()
elif args.command == COMMAND_PUSH_MANIFEST:
    e.push_manifest()
elif args.command == COMMAND_ADD_SUBMODULES:
    e.init_submodules()
elif args.command == COMMAND_DEL_SUBMODULES:
    e.del_submodules()
