@echo off

chcp 65001
color a
cls & title deHasher ^> Компиляция
setlocal enabledelayedexpansion

set "main=main.py"

for %%f in ("*.py") do (
    set "main=%%~nxf"
    goto :found
)
:found

set "basename=%main:.py=%"

set "imports="
if exist imports.txt (
    for /f "tokens=*" %%a in (imports.txt) do (
        set "imports=!imports! --hidden-import=%%a"
    )
)

copy resources\icon.ico icon.ico >nul

pyinstaller --onefile "%main%" --icon=icon.ico !imports!

if exist "dist\%basename%.exe" (
    copy "dist\%basename%.exe" "%basename%.exe" >nul
)

rd /s /q build
rd /s /q dist
del "%basename%.spec" >nul
del icon.ico >nul

echo Компиляция завершена успешно.
pause