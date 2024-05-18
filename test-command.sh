#!/bin/zsh
time maude << EOF
in debug.maude .
in specs/tas.maude
in dca2mc
erew run .
initialize[TAS-CHECK, init, lofree]
layerCheck 2 2
lastCheck
q
EOF

# initialize[TAS-CHECK, init, lofree]
# initialize[TAS-CHECK, init, cstable]
# initialize[TAS-CHECK, init, halt]