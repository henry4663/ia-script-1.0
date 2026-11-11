@echo off
cd /d "%~dp0"
title GameMind AI - CartPole
echo [1/3] Instalando as bibliotecas necessarias...
py -m pip install -r requirements-cartpole.txt
if errorlevel 1 (
  echo ERRO: nao foi possivel instalar as bibliotecas. Confira se o Python e o pip estao instalados.
  pause
  exit /b 1
)
echo.
echo [2/3] Treinando a IA e salvando a memoria...
py cartpole_train.py --episodes 8000
if errorlevel 1 (
  echo ERRO durante o treinamento.
  pause
  exit /b 1
)
echo.
echo [3/3] Abrindo o jogo para a IA jogar...
py cartpole_play.py
pause
