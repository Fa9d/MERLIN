@echo off
REM ============================================================
REM  IVIA - Lance le SITE PUBLIC (frontend statique) en local
REM  Aucune dependance : juste Python. http://localhost:8080
REM ============================================================
cd /d "%~dp0\ivia_site_v2"
echo.
echo  Site IVIA en local : http://localhost:8080
echo  (Ctrl+C pour arreter)
echo.
start "" http://localhost:8080
python -m http.server 8080
