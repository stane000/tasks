@echo off
call ..\app-env\Scripts\activate.bat
pytest city_summary_app_tests.py
pause
