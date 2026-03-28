@echo off

:: Read OLLAMA_MODEL from .env and strip surrounding quotes
for /f "usebackq tokens=1,2 delims==" %%a in (".env") do (
    if "%%a"=="OLLAMA_MODEL" set OLLAMA_MODEL=%%~b
)
if "%OLLAMA_MODEL%"=="" set OLLAMA_MODEL=llama3.2

echo Starting Ollama (Docker)...
docker compose up -d

echo Waiting for Ollama to be ready...
:wait_loop
curl -s http://localhost:11434 >nul 2>&1
if errorlevel 1 (
    timeout /t 2 /nobreak >nul
    goto wait_loop
)

echo Pulling model "%OLLAMA_MODEL%"...
docker compose exec ollama ollama pull %OLLAMA_MODEL%

echo Starting FastAPI (production)...
.venv\Scripts\activate && fastapi run
