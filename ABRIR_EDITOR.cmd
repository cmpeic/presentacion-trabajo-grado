@echo off
setlocal
cd /d "%~dp0"

start "HyperFrames Studio" /B "%~dp0node_modules\.bin\hyperframes.cmd" preview --port 4567 --background --no-open
timeout /t 4 /nobreak >nul
start "" "http://localhost:4567/#project/presentacion-trabajo-grado"

endlocal
exit /b 0
