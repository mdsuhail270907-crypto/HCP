@echo off
echo Starting HPC Cloud Burst Platform...

:: Start the Python backend in a new window
echo Starting Backend Orchestrator...
start cmd /k "pip install -r requirements.txt && python -m backend.app"

:: Start the React frontend in a new window
echo Starting React Frontend...
cd frontend
start cmd /k "npm install && npm run dev"

echo.
echo Both services are booting up!
echo --------------------------------------------------
echo - Backend will be available at: http://127.0.0.1:5000
echo - Frontend will be available at: http://localhost:5173
echo --------------------------------------------------
echo Note: The frontend uses a proxy to automatically communicate with the backend.
echo You can safely close this orchestrator window.
