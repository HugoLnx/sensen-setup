#!/bin/bash
SETUP_ROOT=$(dirname -- "$0")
PROJECT_ROOT=$SETUP_ROOT/..

cd $PROJECT_ROOT

cp $SETUP_ROOT/ConfigFiles/.gitignore .
cp $SETUP_ROOT/ConfigFiles/.editorconfig .
cp $SETUP_ROOT/ConfigFiles/omnisharp.json .
cp $SETUP_ROOT/ConfigFiles/NuGet.config ./Assets/
cp $SETUP_ROOT/ConfigFiles/packages.config ./Assets/
cp $SETUP_ROOT/ConfigFiles/manifest.json ./Packages/
cp -r $SETUP_ROOT/Templates/ProjectStructure/ ./Assets/MY_GAME_NAME/
mkdir ./PackagesBatch/
touch ./PackagesBatch/.gitkeep
mkdir ./Assets/Vendor/
touch ./Assets/Vendor/.gitkeep

git init
git submodule init
git submodule add https://github.com/HugoLnx/unity-lnx-arch.git Assets/Submodules/unity-lnx-arch
git submodule add https://github.com/HugoLnx/sensen-toolkit.git Assets/Submodules/sensen-toolkit
git submodule update --recursive --remote
