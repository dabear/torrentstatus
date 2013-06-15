@echo off
set PYTHONPATH=%PYTHONPATH%;%~dp0
c:\python27\python.exe -m torrentstatus.handle_status_change %*