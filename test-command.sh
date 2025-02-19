#!/bin/zsh
time maude << EOF
load debug.maude .
load specs/qlock.maude
load dca2mc
set-checker spin
set-checker-cores 1
initialize[QLOCK-CHECK, init, lofree]
set-cores 4
layerCheck 2 2
lastCheck
quit
EOF

# set-seed 0
# select 5
# initialize[QLOCK-CHECK, init, halt]
# initialize[QLOCK-CHECK, init, lofree]
# initialize[QLOCK-CHECK, init, cstable]