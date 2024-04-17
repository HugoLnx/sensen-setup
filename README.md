# Environment Setup
## Intro
This document explain how to install your environment with intellisense, analyzers, refactoring and code
styling review. Some things to know...
* It's intended for VS Code.
* The script overwrites a bunch of config files, so be careful. (although backups are created on `bkp/` folder)
* Right now the packages are for 3D, soon enough we'll have an 2D option as well.

## Dependencies
* Python

## Step-by-Step
### Warning
* You need `git-bash` installed if you're on windows
* This script will override the files: `Packages/manifest.json`, `.gitignore`, `.gitattributes`, `.editorconfig`.

### Basic Setup
1. Clone this repository to the root of your project.
```bash
$ git clone git@github.com:HugoLnx/unity-sensen-setup.git
```

2. Use the command that will initialize git
```bash
$ python ./unity-sensen-setup/setup.py git
# This will:
# - Init git
# - Install LFS
# - Create a `.gitignore` fit for unity projects
# - Create a `.gitattributes` fit for unity projects (see section about .gitattributes)
```

3. Commit the whole project
```bash
$ git add .
$ git commit -m "First commit: Through unity-sensen-setup git"
```

4. Execute the initial setup
```bash
$ python ./unity-sensen-setup/setup.py configs --2d --mobile --slim
# This will:
# - Import all configurations
# - Initialize unity-sensen-toolkit submodule
# - Create the ./PackagesBatch/ folder with DOTWeen inside
# Valid Options:
# --2d | --3d | --mobile | --desktop | --slim
# See more on manifest filtering section
```

5. Open the project on Unity
6. Refresh Assets (Press "CTRL + R")
7. At the topbar menu execute: `Tools > Sensen > Resolve Package Manager`
8. Restart Unity
9. Add the unity packages you want into `./PackagesBatch/` folder.
10. At the topbar menu execute: `Tools > Sensen > Import Packages Batch`. (You can also import manually if you want)
11. Execute the full setup
12. (Optional) Open `Unity's Preferences` > Set Visual Studio Code as the External editor, and click in `Regenerate project files`. (Reference: [https://marketplace.visualstudio.com/items?itemName=VisualStudioToolsForUnity.vstuc](Docs Visual Studio Package))
```bash
$ python ./unity-sensen-setup/setup.py structure
# This will:
# - Create project structure on Assets/{Project's folder name}
# - Initialize all pre-defined submodules
# Notes:
# By default, it creates the structure using the same name of the Project's folder, but
# you can specify a custom name using `--name "MyGame"`, this will create the structure
# at `Assets/MyGame`.
```
11. Refresh Assets on Unity (Press "CTRL + R")
12. Commit the setup final state
```bash
$ git add .
$ git commit -m "Complete setup through unity-sensen-setup"
```

### Updating manifest.json
In the `manifest.json` unity keeps the version of the dependencies managed by the Package Manager.
Eventually the versions registered in this repository will get outdated, to update them, you need
to open the Package Manager on Unity, update them one by one, and use the following command:
```bash
$ python ./unity-sensen-setup/setup.py pull-manifest
```

This command will compare your project dependencies with the ones that are set in setup, and will
keep the higher version for all of them. If there's new dependencies in your project, it'll list them
so you can add it to the setup file manually if you want to.

Also, you can update only your project's `manifest.json` by running:
```bash
$ python ./unity-sensen-setup/setup.py push-manifest
```

### .gitattributes
Git attribute is configured to put large file like videos, audio, and 3d models into git LFS. Also
it configures Unity YAML merging on the relevant file types through Unity's official merging tool.
For the merging to work you will need to configure the tool, see more on [https://docs.unity3d.com/Manual/SmartMerge.html](Unity's documentation over Smart Merge).

### Batch *.unitypackage importing
1. Copy the desired `*.unitypackages` to `./PackagesBatch`
2. At the topbar menu execute: `Tools > Sensen > Import Packages Batch`
3. Press "CTRL + R" (Refresh Assets)
4. Move the files related to assets to `/Assets/Vendor` (this folder is in `.gitignore`)

### Manifest filtering
Depending on the project (2d, 3d, mobile, desktop) you'll probably need a different set of
dependencies. For that reason, all commands that pushed the manifest can receive one of the
following options:
* `--2d`: Forces it to add 2D dependencies and exclude 3D-only dependencies
* `--3d`: Forces it to add 3D dependencies and exclude 2D-only dependencies
* `--mobile`: Forces it to add mobile-only dependencies
* `--desktop`: Forces it to exclude mobile-only dependencies
* `--slim`: Removes dependencies that usually won't be used in prototypes and
gamejam projects. (eg. localization, analytics, testing, profilling tools, etc)


_PS.: If you don't pass any options explicitly the script will try to guess based on the project's
dependencies._

## VS Code extra config
### Suggested Extensions
- C# Dev Kit by Microsoft
    - C# by Microsoft
    - IntelliCode for C# Dev Kit
- Unity by Microsoft
- Editor Config
- GitLens
- Material Icon Theme
- Unity Toolbox
- Unity Tools
- Github Copilot

### Some keys on my `settings.json`
```JSON
    "unityToolbox.privateAccessModifier": true,
    "unity-tools.documentationVersion": "2022.3",
    "unity-tools.localDocumentationViewer": "chrome",
    "material-icon-theme.folders.associations": {
        "Art": "Theme",
        "Textures": "Images",
        "Sprites": "Images",
        "Musics": "Audio",
        "Models": "Fastlane",
        "UI": "Aurelia",
        "Materials": "Archive",
        "Scriptables": "Mock",
        "Scripts": "Quasar",
        "Submodules": "Git",
        "StateGraphs": "Context",
        "Inputs": "Download",
        "Maps": "Base",
        "Prefabs": "Node",
        "Scenes": "Storybook",
        "Timelines": "Update"
    },
    "editor.rulers": [
        80,
        100,
        120
    ],
```

## What's installed on the Package Manager...
Unity Packages
- Cinemachine
- Editor Coroutines
- Unity Profiling Core API
- Unity UI
- Addressables
- Analytics
- Burst
- Collections
- Input System
- Localization
- Mathematics
- Post Processing
- [3D] ProGrids: https://docs.unity3d.com/Packages/com.unity.progrids@3.0/manual/index.html


- Cinematic Studio
- Engineering
- Gameplay and Storytelling
- [3D] 3D Characters and Animations
- [3D] 3D World Building


## Some Packages we plan to put in our private collection...
Asset Store - Paid
- InControl
- Odin
- Bayat - Save System
- Dialogue System for Unity
- Better UI

Asset Store - Free
- DOTween (HOTween v2)
- Fast Script Reload


VFX - Paid
- Epic Toon FX
- Inferno VFX
- RPG VFX Bundle
- RTS FX
- Sci-Fi Arsenal
- Ultimate VFX
- Quibli: Anime Shaders and Tools
- Underwater FX

VFX - Free
- Free Skybox Extended Shader
- Particle Pack

## TODO: Check would be better to create a Unity Template
