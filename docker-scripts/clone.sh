#!/bin/sh

set -e

LOCALREPO=/ext-src/$DET_LOCALSRC

if [ ! -d $LOCALREPO ]
then
    git clone $DET_REPOS_PATCH_URL $LOCALREPO
    cd $LOCALREPO
    git config user.name "$DET_REPOS_USER_NAME"
    git config user.email "$DET_REPOS_USER_EMAIL"
else
    cd $LOCALREPO
    git pull --rebase $DET_REPOS_PATCH_URL
fi
git pull --rebase $DET_REPOS_MATRIX_URL $DET_REPOS_MATRIX_BRANCH
