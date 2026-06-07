# Trip Dreams

Trip Dreams is a group travel planning app built with FastAPI, Firestore, and a simple HTML/CSS/JavaScript frontend.

## What is included

- `main.py` — FastAPI backend serving the homepage and API endpoints
- `static/` — frontend files for the landing page and dream planner UI
- `requirements.txt` — Python dependencies
- `.gitignore` — ignores `.venv` and Python cache files

## Run locally

1. Activate the virtual environment:
   - PowerShell: `.\.venv\Scripts\Activate.ps1`
   - Command Prompt: `.\.venv\Scripts\activate.bat`
2. Run the app:
   - `.\.venv\Scripts\python.exe -m uvicorn main:app --reload --host 127.0.0.1 --port 8000`
3. Open in your browser:
   - `http://127.0.0.1:8000`

## What to build next

1. Connect Firestore with real data storage
2. Add Google OAuth for secure login
3. Build group profiles and trip sharing
4. Add Google Calendar syncing for availability

## Notes

- The app currently uses a local in-memory fallback if Firestore credentials are not configured.
- To enable Firestore, set `GOOGLE_CREDENTIALS_JSON` in your environment with your service account JSON.
