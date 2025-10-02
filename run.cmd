@echo off
setlocal EnableDelayedExpansion

rem Prefer UV_PATH from environment; otherwise try to read from .env
if not defined UV_PATH (
  if exist ".env" (
    for /f "usebackq eol=# tokens=1,* delims==" %%A in (".env") do (
      set "key=%%~A"
      if /I "!key!"=="UV_PATH" (
        set "UV_PATH=%%~B"
      )
    )
    rem strip quotes if present
    if defined UV_PATH set "UV_PATH=!UV_PATH:\"=!"
    rem treat empty or just a dot as undefined
    if not defined UV_PATH set "UV_PATH="
    if /I "!UV_PATH!"=="." set "UV_PATH="
  )
)

rem Fallback default path if still not set
if not defined UV_PATH set "UV_PATH=C:\Users\sukum\.local\bin\uv.exe"
if not exist "%UV_PATH%" (
  echo uv.exe not found at %UV_PATH%. Install uv or update run.cmd.
  exit /b 1
)
"%UV_PATH%" run main.py %*
exit /b %errorlevel%
