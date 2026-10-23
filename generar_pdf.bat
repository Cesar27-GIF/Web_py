@echo off
title Generando PDF del Ensayo - Portal IA
color 0A
echo ===================================================
echo  Generando static\Ensayo_Etica_IA.pdf ...
echo  (documento A4 desde ensayo.py via /ensayo/imprimir)
echo ===================================================
cd /d "%~dp0"

REM Servidor temporal en el puerto 5001
start "" /B python -c "from app import app; app.run(host='127.0.0.1', port=5001)" >nul 2>&1
timeout /t 4 /nobreak >nul

set "PDF=%~dp0static\Ensayo_Etica_IA.pdf"
set "URL=http://127.0.0.1:5001/ensayo/imprimir"

set "CHROME="
if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" set "CHROME=%ProgramFiles%\Google\Chrome\Application\chrome.exe"
if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" set "CHROME=%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
if not defined CHROME if exist "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" set "CHROME=%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"
if exist "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe" set "CHROME=%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"

if not defined CHROME (
    echo [ERROR] No se encontro Chrome ni Edge en este equipo.
    goto :fin
)

echo Generando con: "%CHROME%"
"%CHROME%" --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf="%PDF%" "%URL%"

REM Apagar el servidor temporal del puerto 5001
for /f "tokens=5" %%a in ('netstat -a -n -o ^| findstr :5001 ^| findstr LISTENING') do taskkill /F /PID %%a >nul 2>&1

if exist "%PDF%" (
    echo.
    echo  PDF generado correctamente: static\Ensayo_Etica_IA.pdf
    echo  Refresca la seccion de Ensayo en la web para verlo.
) else (
    echo.
    echo  [ERROR] No se genero el PDF.
)
:fin
echo.
pause
