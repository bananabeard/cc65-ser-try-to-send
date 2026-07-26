#!/bin/bash

set -e

CC65_HOME="$(readlink -m ..)"

rm -f *.prg

"${CC65_HOME}/bin/cl65" \
    -I "${CC65_HOME}/include" \
    -L "${CC65_HOME}/lib" \
    -t c64 \
    -Or -Os \
    -o terminal-do-not-try-to-send.prg \
    terminal.c

"${CC65_HOME}/bin/cl65" \
    -I "${CC65_HOME}/include" \
    -L "${CC65_HOME}/lib" \
    -DSER_TRY_TO_SEND=1 \
    -t c64 \
    -Or -Os \
    -o terminal-do-try-to-send.prg \
    terminal.c
