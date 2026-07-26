#!/bin/bash
x64sc \
    -acia1 \
    -acia1base 0xDE00 \
    -acia1irq 1 \
    -acia1mode 1 \
    -myaciadev 2 \
    +keyset \
    -maximized \
    -rsdev3 "127.0.0.1:12345" \
    -rsdev3baud 38400 \
    "$1"
