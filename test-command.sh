#!/bin/zsh
time maude << EOF
load debug.maude .
load specs/ticket.maude
load dca2mc
set-checker spin
set-checker-cores 8
initialize[TICKET-CHECK, init9, lofree]
set-cores 8
layerCheck 2 2
lastCheck
quit
EOF

# set-seed 0
# select 5
# initialize[QLOCK-CHECK, init, halt]
# initialize[QLOCK-CHECK, init, lofree]
# initialize[QLOCK-CHECK, init, cstable]