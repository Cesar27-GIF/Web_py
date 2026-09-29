@echo off
title Servidor Web - Portal Educativo de IA
color 0A
echo ===================================================
echo  Iniciando Servidor Web de IA (Flask)...
echo  Modulos: Glosario, Linea de Tiempo, Clasificacion,
echo           Machine Learning y Ensayo de Etica
echo ===================================================
echo.
cd /d "%~dp0"
python app.py
pause
