#!/bin/bash
SETUP_ROOT=$(dirname -- "$0")
PROJECT_ROOT=$SETUP_ROOT/..
BKP_FOLDER=$SETUP_ROOT/bkp/

cd $PROJECT_ROOT

# BACKUP CONFIG FILES
timestamp=$(date +%Y%m%d%H%M%S)
mkdir -p $BKP_FOLDER

function backupFileIfExists() {
    filename=$1
    # get second argument or default to "."
    filefolder=${2:-"."}
    filepath=$filefolder/$1
    if [ -f $filepath ];then
        echo "Backing up $filename in ./sensen-setup/bkp/"
        cp -rf $filepath $BKP_FOLDER/${timestamp}_$filename
    fi
}

backupFileIfExists ".gitignore"
backupFileIfExists ".editorconfig"
backupFileIfExists "omnisharp.json"
backupFileIfExists "NuGet.config" "Assets/"
backupFileIfExists "packages.config" "Assets/"
backupFileIfExists "manifest.json" "Packages/"

# REPLACE CONFIG FILES
cp $SETUP_ROOT/ConfigFiles/.gitignore .
if [[ -z "${ONLY_GIT}" ]]; then
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
fi

git init
if [[ -z "${ONLY_GIT}" ]]; then
    git submodule init
    git submodule add https://github.com/HugoLnx/unity-lnx-arch.git Assets/Submodules/unity-lnx-arch
    git submodule add https://github.com/HugoLnx/sensen-toolkit.git Assets/Submodules/sensen-toolkit
    git submodule update --recursive --remote
    echo "Full setup finished."
else
    echo "Only Git was initialized."
fi
