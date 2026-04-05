import sqlite3
import threading


class SQLiteDB:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, db_path="/home/deepak/projects/Memora/logs.db"):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(SQLiteDB, cls).__new__(cls)
                    cls._instance._init(db_path)
        return cls._instance

    def _init(self, db_path):
        self.conn = sqlite3.connect(
            db_path,
            check_same_thread=False
        )
        self.conn.row_factory = sqlite3.Row

    def execute(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor

    def fetchone(self, query, params=()):
        cursor = self.execute(query, params)
        return cursor.fetchone()

    def fetchall(self, query, params=()):
        cursor = self.execute(query, params)
        return cursor.fetchall()

    def close(self):
        self.conn.close()
        SQLiteDB._instance = None


db = SQLiteDB("/home/deepak/projects/Memora/logs.db")