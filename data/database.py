"""
database.py — SQLite Database Layer
Persists scenario, task, and result data.
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "alb_data.db")


def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db(db_path: str = DB_PATH) -> None:
    """Create tables if they don't exist."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS scenarios (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            cycle_time  REAL NOT NULL,
            algorithm   TEXT NOT NULL DEFAULT 'rpw',
            created_at  TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS tasks (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            scenario_id     INTEGER NOT NULL,
            task_id         TEXT NOT NULL,
            task_name       TEXT NOT NULL,
            duration        REAL NOT NULL,
            predecessors    TEXT DEFAULT '',
            FOREIGN KEY (scenario_id) REFERENCES scenarios(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS results (
            id                      INTEGER PRIMARY KEY AUTOINCREMENT,
            scenario_id             INTEGER NOT NULL UNIQUE,
            num_stations            INTEGER,
            line_efficiency         REAL,
            balance_delay           REAL,
            smoothness_index        REAL,
            theoretical_min         INTEGER,
            total_energy_kwh        REAL DEFAULT 0,
            total_co2_kg            REAL DEFAULT 0,
            total_cost              REAL DEFAULT 0,
            stations_json           TEXT,
            created_at              TEXT NOT NULL,
            FOREIGN KEY (scenario_id) REFERENCES scenarios(id) ON DELETE CASCADE
        );
    """)
    conn.commit()
    conn.close()


# ------------------------------------------------------------------ #
#  Scenario CRUD
# ------------------------------------------------------------------ #

def save_scenario(
    name: str,
    cycle_time: float,
    algorithm: str,
    tasks_data: List[Dict],
    metrics: Dict[str, Any],
    stations: List[Dict],
    energy_report: Optional[Dict] = None,
    db_path: str = DB_PATH,
) -> int:
    """Save a complete scenario: scenario + tasks + results."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    now = datetime.now().isoformat()

    # Main scenario record
    cursor.execute(
        "INSERT INTO scenarios (name, cycle_time, algorithm, created_at) VALUES (?, ?, ?, ?)",
        (name, cycle_time, algorithm, now),
    )
    scenario_id = cursor.lastrowid

    # Tasks
    for t in tasks_data:
        preds = t.get("predecessors", "")
        if isinstance(preds, list):
            preds = " ".join(preds)
        cursor.execute(
            "INSERT INTO tasks (scenario_id, task_id, task_name, duration, predecessors) "
            "VALUES (?, ?, ?, ?, ?)",
            (scenario_id, t["task_id"], t["task_name"], t["duration"], preds),
        )

    # Results
    energy = energy_report or {}
    cursor.execute(
        "INSERT INTO results "
        "(scenario_id, num_stations, line_efficiency, balance_delay, "
        "smoothness_index, theoretical_min, total_energy_kwh, total_co2_kg, "
        "total_cost, stations_json, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            scenario_id,
            metrics.get("num_stations", 0),
            metrics.get("line_efficiency", 0),
            metrics.get("balance_delay", 0),
            metrics.get("smoothness_index", 0),
            metrics.get("theoretical_min_stations", 0),
            energy.get("total_energy_kwh", 0),
            energy.get("total_co2_kg", 0),
            energy.get("total_cost", 0),
            json.dumps(stations, ensure_ascii=False),
            now,
        ),
    )

    conn.commit()
    conn.close()
    return scenario_id


def list_scenarios(db_path: str = DB_PATH) -> List[Dict]:
    """List all scenarios."""
    conn = get_connection(db_path)
    rows = conn.execute(
        "SELECT s.*, r.line_efficiency, r.num_stations "
        "FROM scenarios s LEFT JOIN results r ON s.id = r.scenario_id "
        "ORDER BY s.created_at DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def load_scenario(scenario_id: int, db_path: str = DB_PATH) -> Optional[Dict]:
    """Load a scenario with all details."""
    conn = get_connection(db_path)

    scenario = conn.execute(
        "SELECT * FROM scenarios WHERE id = ?", (scenario_id,)
    ).fetchone()
    if not scenario:
        conn.close()
        return None

    tasks = conn.execute(
        "SELECT * FROM tasks WHERE scenario_id = ? ORDER BY task_id",
        (scenario_id,),
    ).fetchall()

    result = conn.execute(
        "SELECT * FROM results WHERE scenario_id = ?", (scenario_id,)
    ).fetchone()

    conn.close()

    data = dict(scenario)
    data["tasks"] = [dict(t) for t in tasks]
    data["results"] = dict(result) if result else None
    if data["results"] and data["results"].get("stations_json"):
        data["results"]["stations"] = json.loads(data["results"]["stations_json"])

    return data


def delete_scenario(scenario_id: int, db_path: str = DB_PATH) -> bool:
    """Delete scenario (CASCADE deletes tasks and results too)."""
    conn = get_connection(db_path)
    cursor = conn.execute("DELETE FROM scenarios WHERE id = ?", (scenario_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted
