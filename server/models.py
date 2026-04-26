from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Machine(Base):
    __tablename__ = 'machines'
    machine_id = Column(String, primary_key=True) # SHA-256 of MAC
    os = Column(String, nullable=False) # 'windows' | 'linux'
    hostname_hash = Column(String, nullable=False) # SHA-256(hostname)
    cpu_cores = Column(Integer)
    ram_total_mb = Column(Integer)
    timezone = Column(String) # e.g. 'Africa/Douala'
    city = Column(String)
    registered_at = Column(DateTime, default=datetime.datetime.utcnow)

    sessions = relationship("Session", back_populates="machine")
    snapshots = relationship("Snapshot", back_populates="machine")
    power_events = relationship("PowerEvent", back_populates="machine")

class Session(Base):
    __tablename__ = 'sessions'
    session_id = Column(String, primary_key=True) # UUID v4
    machine_id = Column(String, ForeignKey('machines.machine_id'), nullable=False)
    boot_time = Column(DateTime, nullable=False)
    shutdown_time = Column(DateTime)
    active = Column(Boolean, default=True)
    shutdown_type = Column(String) # 'clean' | 'power_cut' | 'unknown'
    power_cut_detected = Column(Boolean, default=False)
    power_cut_gap_s = Column(Integer)
    uptime_seconds = Column(Integer)

    machine = relationship("Machine", back_populates="sessions")
    snapshots = relationship("Snapshot", back_populates="session")

class Snapshot(Base):
    __tablename__ = 'snapshots'
    snapshot_id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey('sessions.session_id'), nullable=False)
    machine_id = Column(String, ForeignKey('machines.machine_id'), nullable=False)
    ts_utc = Column(DateTime, nullable=False)
    ts_local = Column(DateTime, nullable=False)
    day_of_week = Column(Integer, nullable=False)
    hour_of_day = Column(Integer, nullable=False)
    
    # Resources
    cpu_percent = Column(Float)
    cpu_freq_mhz = Column(Float)
    ram_available_mb = Column(Integer)
    ram_percent_used = Column(Float)
    disk_read_mbps = Column(Float)
    disk_write_mbps = Column(Float)
    
    # Power
    battery_percent = Column(Float)
    power_plugged = Column(Boolean)

    # Connectivity
    is_connected = Column(Boolean, default=False)
    network_latency_ms = Column(Float)
    bytes_sent_kb = Column(Integer)
    bytes_recv_kb = Column(Integer)
    
    # User activity
    user_active = Column(Boolean)
    idle_seconds = Column(Integer)
    screen_on = Column(Boolean)
    
    # Agent state
    synthetic_task_active = Column(Boolean, default=False)
    synced = Column(Boolean, default=False)

    session = relationship("Session", back_populates="snapshots")
    machine = relationship("Machine", back_populates="snapshots")

Index('idx_snap_machine', Snapshot.machine_id, Snapshot.ts_utc)
Index('idx_snap_synced', Snapshot.synced)

class PowerEvent(Base):
    __tablename__ = 'power_events'
    event_id = Column(Integer, primary_key=True, autoincrement=True)
    machine_id = Column(String, ForeignKey('machines.machine_id'), nullable=False)
    event_type = Column(String, nullable=False) # 'power_cut' | 'to_battery' | 'to_ac'
    detected_at = Column(DateTime, nullable=False)
    last_heartbeat_ts = Column(DateTime)
    gap_seconds = Column(Integer)
    cpu_before = Column(Float)
    ram_before = Column(Float)

    machine = relationship("Machine", back_populates="power_events")

class TaskResult(Base):
    __tablename__ = 'task_results'
    task_id = Column(String, primary_key=True) # UUID v4
    machine_id = Column(String, ForeignKey('machines.machine_id'), nullable=False)
    session_id = Column(String, ForeignKey('sessions.session_id'), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    target_duration_s = Column(Integer)
    actual_duration_s = Column(Integer)
    interrupted = Column(Boolean, default=False)
    avg_cpu_load = Column(Float)
    avg_ram_load = Column(Float)
    network_io_mb = Column(Float)

    machine = relationship("Machine")
    session = relationship("Session")

class SyncLog(Base):
    __tablename__ = 'sync_log'
    sync_id = Column(Integer, primary_key=True, autoincrement=True)
    machine_id = Column(String, ForeignKey('machines.machine_id'), nullable=False)
    synced_at = Column(DateTime, default=datetime.datetime.utcnow)
    rows_sent = Column(Integer, nullable=False)
    status = Column(String, nullable=False) # 'ok' | 'fail' | 'partial'
    error_msg = Column(Text)
