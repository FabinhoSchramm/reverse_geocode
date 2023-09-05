#!/bin/bash

PATH=$(pwd)

alias open=xdg-open

. venv/bin/activate

venv/bin/python3 reverse_geocode.py &
PID1=$!

wait $PID1