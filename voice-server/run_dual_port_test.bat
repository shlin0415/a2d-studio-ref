@echo off
chcp 65001 >nul
set PYTHONUTF8=1
call conda activate a2d-studio
cd /d "%~dp0"
python test_dual_port_performance.py
pause
