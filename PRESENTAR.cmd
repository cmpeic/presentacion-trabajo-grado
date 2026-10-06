@echo off
setlocal
cd /d "%~dp0"

set "PUERTO=4600"
set "URL=http://localhost:%PUERTO%/presentar.html"

echo Iniciando el reproductor en %URL%
start "Servidor presentacion" /MIN cmd /c "node servidor.js %PUERTO%"

timeout /t 2 /nobreak >nul

set "CHROME=%ProgramFiles%\Google\Chrome\Application\chrome.exe"
if not exist "%CHROME%" set "CHROME=%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
set "EDGE=%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"
if not exist "%EDGE%" set "EDGE=%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"

if exist "%CHROME%" (
  start "" "%CHROME%" --app=%URL% --start-fullscreen
) else if exist "%EDGE%" (
  start "" "%EDGE%" --app=%URL% --start-fullscreen
) else (
  start "" "%URL%"
)

echo Enter / Clic = Avanzar lamina    Flecha Izq / Backspace = Retroceder
echo Espacio / Flecha Der = Avanzar    M = Modo Manual/Auto    F = Pantalla completa
echo Cierre esta ventana o pulse Ctrl+C para detener el servidor.
echo.
endlocal
exit /b 0
