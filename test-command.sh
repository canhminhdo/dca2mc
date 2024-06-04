#!/bin/zsh
time maude << EOF
load debug.maude .
load specs/qlock.maude
load dca2mc
initialize[QLOCK-CHECK, init, lofree]
layerCheck 2 2
lastCheck
q
EOF

# initialize[QLOCK-CHECK, init, halt]
# initialize[QLOCK-CHECK, init, lofree]
# initialize[QLOCK-CHECK, init, cstable]