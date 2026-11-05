@echo off
title Servidor Web - Portal Educativo de IA
color 0A
echo ===================================================
echo  Iniciando Servidor Web de IA (Flask)...
echo  Modulos: Glosario, Linea de Tiempo, Clasificacion,
echo           Algoritmos de Busqueda, Machine Learning, Ensayo de Etica y Clasificador ML for Kids
echo ===================================================
echo.
cd /d "%~dp0"
python app.py
pause
