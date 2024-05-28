#!/bin/zsh
time maude << EOF
load debug.maude .
load specs/tas.maude
load dca2mc
initialize[TAS-CHECK, init, lofree]
set-cores 2
layerCheck 2 2
lastCheck
q
EOF

# initialize[TAS-CHECK, init, lofree]
# initialize[TAS-CHECK, init, cstable]
# initialize[TAS-CHECK, init, halt]