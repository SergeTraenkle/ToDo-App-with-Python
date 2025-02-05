import sqlite3
import dataclasses
from typing import List

@dataclasses.dataclass
class Task:
    id: int = None
    text: str = ""
    done: bool = False

class DB_Service:
    def __init__(self, db_name='tasks.db'):
        self.db_name = db_name
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                text TEXT NOT NULL,
                done BOOLEAN NOT NULL
                )
            ''')
            conn.commit()

    def insert(self, task: Task) -> Task:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO tasks (text, done) VALUES (?, ?)',
                           (task.text, task.done))
            conn.commit()
            task.id = cursor.lastrowid
        return task

    def update(self, task: Task):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE tasks SET text = ?, done = ? WHERE id = ?',
                           (task.text, task.done, task.id))
            conn.commit()

    def delete(self, task: Task):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task.id,))
            conn.commit()

    def fetchAll(self) -> List[Task]:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, text, done FROM tasks')
            rows = cursor.fetchall()
            return [Task(id=row[0], text=row[1], done=bool(row[2]))
                    for row in rows]
