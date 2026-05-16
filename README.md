# Virtual-Power-Plant-Management-System

A working Virtual Power Plant management system with a Python backend and a frontend dashboard.

## Project Structure

- `backend/`
  - `config.yaml` — market pricing and battery parameters
  - `database.py` — SQLite models for battery telemetry and energy logs
  - `data_loader.py` — mock daily load and PV profile generator
  - `optimizer.py` — dispatch scheduler with demand response logic
  - `finance.py` — session revenue and cost summary
  - `alerts.py` — in-memory alert manager
  - `forecaster.py` — mock load forecast generator
  - `iot_simulator.py` — simulated battery telemetry and energy logs
  - `main.py` — FastAPI application entry point
  - `requirements.txt` — backend dependencies
  - `__init__.py` — package marker for backend imports
- `frontend/`
  - `index.html` — static Vue.js dashboard for telemetry, dispatch and alerts

## Requirements

Install the backend dependencies before running the service:

```bash
cd /workspaces/Virtual-Power-Plant-Management-System
python3 -m pip install -r backend/requirements.txt
```

If you prefer a virtual environment, activate it first.

## Run the backend

From the repo root:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://127.0.0.1:8000/`.

## Use the dashboard

Open `frontend/index.html` in a browser or serve it with a static file server.
The frontend communicates with the backend at `http://127.0.0.1:8000`.

## API Endpoints

- `GET /telemetry` — latest battery state
- `GET /dispatch?dr_active=false|true` — generate a dispatch plan
- `GET /finance` — session-level profit/cost summary
- `GET /alerts` — active system alerts
- `GET /forecast` — mock next-day load forecast

## Notes

- `backend/optimizer.py` now loads `backend/config.yaml` reliably and uses the configured `buy_price` and `sell_price` keys.
- `frontend/index.html` no longer calls the dispatch endpoint twice.
- The backend is intended for development and demo use.
