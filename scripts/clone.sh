#!/bin/sh

set -e

LOCALREPO=/ext-src/$DET_LOCALSRC

if [ ! -d $LOCALREPO ]
then
    git clone $DET_REPOSURL $LOCALREPO
else
    cd $LOCALREPO
    git pull --rebase $DET_REPOSURL
fi
