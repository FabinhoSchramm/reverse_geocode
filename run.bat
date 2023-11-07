@echo off

REM Ativar o ambiente virtual
call ./venv/bin/activate

REM Executar o script Python
python reverse_geocode.py

pause

REM Desativar o ambiente virtual (opcional)
deactivate