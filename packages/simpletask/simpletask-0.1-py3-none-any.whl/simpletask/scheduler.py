import sqlite3
import threading
from datetime import datetime, timedelta, time

class TaskScheduler:
    def __init__(self, db_path="tasks.db"):
        self.tasks = []
        self._stop_event = threading.Event()
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS task_logs (
            task_name TEXT PRIMARY KEY,
            last_run TEXT,
            next_run TEXT
        )
        """)

    def add_task(self, func, interval=None, daily_at=None):
        task = {
            "func": func,
            "interval": interval,
            "daily_at": daily_at,
            "name": func.__name__
        }
        self._load_task_state(task)
        self.tasks.append(task)

    def _load_task_state(self, task):
        cursor = self.conn.execute(
            "SELECT last_run, next_run FROM task_logs WHERE task_name = ?",
            (task["name"],)
        )
        row = cursor.fetchone()
        if row:
            task["last_run"] = datetime.fromisoformat(row[0]) if row[0] else None
            task["next_run"] = datetime.fromisoformat(row[1]) if row[1] else None

    def _save_task_state(self, task):
        self.conn.execute(
            "INSERT OR REPLACE INTO task_logs (task_name, last_run, next_run) VALUES (?, ?, ?)",
            (task["name"], 
             task["last_run"].isoformat() if task["last_run"] else None,
             task["next_run"].isoformat() if task["next_run"] else None)
        )
        self.conn.commit()

    def _calculate_next_run(self, task):
        now = datetime.now()
        if task["interval"]:
            next_run = (task["last_run"] or now) + timedelta(seconds=task["interval"])
        elif task["daily_at"]:
            hour, minute = map(int, task["daily_at"].split(":"))
            next_run = now.replace(hour=hour, minute=minute, second=0)
            if next_run < now:
                next_run += timedelta(days=1)
        return next_run

    def _run_task(self, task):
        while not self._stop_event.is_set():
            now = datetime.now()
            if not task.get("next_run"):
                task["next_run"] = self._calculate_next_run(task)

            if now >= task["next_run"]:
                try:
                    task["func"]()
                    task["last_run"] = now
                    task["next_run"] = self._calculate_next_run(task)
                    self._save_task_state(task)
                except Exception as e:
                    print(f"Error en tarea {task['name']}: {e}")
            time.sleep(1)

    def start(self):
        for task in self.tasks:
            thread = threading.Thread(target=self._run_task, args=(task,), daemon=True)
            thread.start()

    def stop(self):
        self._stop_event.set()
        self.conn.close()