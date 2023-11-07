#!/bin/bash

PATH=$(pwd)

# Ativar o ambiente virtual
source $PATH/venv/bin/activate 

python3 reverse_geocode.py &
PID1=$!

wait $PID1

# Desativar o ambiente virtual (opcional)
deactivate