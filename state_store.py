import sqlite3
from pathlib import Path

def db_path(root: Path): return root / '.sync_state.db'

def init_db(root: Path):
    c=sqlite3.connect(db_path(root))
    c.execute('CREATE TABLE IF NOT EXISTS runs(id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, source TEXT, target TEXT, summary_json TEXT)')
    c.commit(); c.close()

def add_run(root: Path, ts: str, source: str, target: str, summary_json: str):
    init_db(root)
    c=sqlite3.connect(db_path(root))
    c.execute('INSERT INTO runs(ts,source,target,summary_json) VALUES (?,?,?,?)',(ts,source,target,summary_json))
    c.commit(); c.close()

def list_runs(root: Path, limit=20):
    init_db(root)
    c=sqlite3.connect(db_path(root))
    rows=c.execute('SELECT id,ts,source,target,summary_json FROM runs ORDER BY id DESC LIMIT ?', (limit,)).fetchall()
    c.close(); return rows
