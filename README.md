# Virtual-Power-Plant-Management-System
We will use a Python backend for the energy management logic (due to its strong libraries for scientific computing and optimization) and a Vue.js frontend for the dashboard.

vpp_system/
├── backend/
│   ├── config.yaml          # System configuration (prices, capacities)
│   ├── data_loader.py       # Handles mock data generation (Load/PV)
│   ├── optimizer.py         # The core "Brain" (Optimization logic)
│   ├── main.py              # FastAPI application entry point
│   └── requirements.txt     # Python dependencies
└── frontend/
    └── index.html           # Simple Vue.js Dashboard

vpp_system/
├── backend/
│   ├── config.yaml
│   ├── database.py          # [NEW] SQLite Setup & Models
│   ├── iot_simulator.py     # [NEW] Real-time data generator
│   ├── optimizer.py         # [UPDATED] Includes DR logic
│   ├── main.py              # [UPDATED] Adds new endpoints
│   └── requirements.txt
└── frontend/
    └── index.html           # [UPDATED] Adds charts & DR button

vpp_system/
├── backend/
│   ├── config.yaml
│   ├── database.py          # Updated with Revenue models
│   ├── iot_simulator.py
│   ├── optimizer.py
│   ├── main.py
│   ├── finance.py           # [NEW] Revenue & Settlement logic
│   ├── alerts.py            # [NEW] Notification system
│   └── forecaster.py        # [NEW] Load prediction
└── frontend/
    └── index.html           # [UPDATED] Financial dashboard & Alerts