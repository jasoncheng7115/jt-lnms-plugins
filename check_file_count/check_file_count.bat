@echo off
rem SPDX-License-Identifier: AGPL-3.0-or-later
rem --------------------------------------------
rem check_file_count.bat  v1.0
rem  Author: Jason Cheng (Jason Tools), jason@jason.tools
rem  https://github.com/jasoncheng7115/jt-lnms-plugins
rem  Argument: %1 = folder to check (e.g. d:\a)
rem  Plain CMD, single file: dir + find, no PowerShell needed
rem --------------------------------------------
setlocal enabledelayedexpansion

rem Target folder
set "DIR=%~1"

rem 1. Folder must exist and be readable
if not exist "%DIR%" (
    echo CRITICAL - directory "%DIR%" does not exist or cannot be accessed
    exit /b 2
)

rem 2. List all files (not folders), errors to nul, count the lines with find
for /f %%A in (
    'dir /b /a-d /s "%DIR%" 2^>nul ^| find /c /v ""'
) do set "COUNT=%%A"

rem 3. Return the state from the file count
if "%COUNT%"=="0" (
    echo OK - no files in "%DIR%"
    exit /b 0
) else (
    echo CRITICAL - %COUNT% files found in "%DIR%"
    exit /b 2
)
