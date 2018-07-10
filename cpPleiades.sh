#/bin/bash

rsync -vr -e 'ssh -p 22022' --exclude='.*' --exclude='__pycache__' src cpPleiades.sh mauraisa@pleiades.bc.edu:~/local/getResidueNumbers/

