# Environment Setup
## Intro
This document explain how to install your environment with intellisense omnisharp, analyzers, refactoring and code
styling review. Some things to know...
* It's intended for VS Code.
* The script overwrites a bunch of config files, so be careful.
* Right now the packages are for 3D, soon enough we'll have an 2D option as well.


## Step-by-Step
### Warning
* You need `git-bash` installed if you're on windows
* This script will override the files: `Packages/manifest.json`, `.gitignore`, `.editorconfig`, `omnisharp.json`,
`Assets/NuGet.config` and `Assets/packages.config`.

### Basic Setup
1. Copy this folder to the root of your project
2. Run `./sensen-setup/setup.sh`
3. Open the Unity project
4. Press "CTRL + R" (Refresh Assets)
5. At the topbar menu execute: `Tools > Sensen > Resolve Package Manager`
6. Restart Unity and VsCode

### Batch *.unitypackage importing
1. Copy the desired `*.unitypackages` to `./PackagesBatch`
2. At the topbar menu execute: `Tools > Sensen > Import Packages Batch`
3. Press "CTRL + R" (Refresh Assets)
4. Move the files related to assets to `/Assets/Vendor` (this folder is in `.gitignore`)

## VS Code extra config
### Suggested Extensions
- C# (powered by OmniSharp)
- GitLens
- Material Icon Theme
- Unity Toolbox
- Unity Tools
- Gitlab Copilot

### Some keys on my `settings.json`
```JSON
    "unityToolbox.privateAccessModifier": true,
    "unity-tools.documentationVersion": "2021.3",
    "unity-tools.localDocumentationViewer": "chrome",
    "omnisharp.enableRoslynAnalyzers": true,
    "omnisharp.analyzeOpenDocumentsOnly": true,
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
NuGet Packages
- Microsoft.CodeAnalysis.CSharp
- Microsoft.CodeAnalysis.CSharp.CodeStyle
- Microsoft.CodeAnalysis.FxCopAnalyzers
- Microsoft.Unity.Analyzers
- Roslynator.Analyzers
- Roslynator.Formatting.Analyzers
- Roslynator.CodeAnalysis.Analyzers

Unity Packages
- NuGetForUnity
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
