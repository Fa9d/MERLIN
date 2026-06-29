@echo off
REM ============================================================
REM  IVIA / MERLIN - Synchronisation locale <- GitHub
REM  Double-clic = recupere les dernieres modifs (Perplexity,
REM  Copilot, Claude Code) depuis la branche canonique.
REM  Source unique : Fa9d/MERLIN @ refonte-ivia-site-unifie
REM ============================================================
cd /d "%~dp0"

echo.
echo === 1) Recuperation depuis GitHub (git pull) ===
git pull --ff-only
if errorlevel 1 (
  echo.
  echo  !! Le pull n'a pas pu se faire en fast-forward.
  echo  !! Tu as probablement des modifications locales non sauvegardees.
  echo  !! Fais "git status" pour voir, ou demande a Claude Code.
)

echo.
echo === 2) Etat actuel du dossier ===
git status -sb

echo.
echo === 3) Branche et dernier commit ===
git log -1 --format="%%h  %%s  (%%cd)" --date=short

echo.
echo Termine. (Pour ENVOYER tes modifs vers GitHub : git push)
pause
