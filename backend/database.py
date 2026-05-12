# backend/database.py
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./vpp_data.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class BatteryStatus(Base):
    __tablename__ = "battery_status"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.now)
    soc_percent = Column(Float) # State of Charge %
    power_kw = Column(Float)    # Current Power (Positive=Charge, Negative=Discharge)
    mode = Column(String)       # "IDLE", "CHARGE", "DISCHARGE", "DR_EVENT"

class EnergyLog(Base):
    __tablename__ = "energy_logs"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.now)
    pv_generation = Column(Float)
    load_consumption = Column(Float)
    grid_import = Column(Float)
    cost = Column(Float)

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()