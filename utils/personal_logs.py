from db.db_sql import SQLiteDB
from schemas.log import LogCreate,LogResponse

def create_logs_table(db: SQLiteDB):
    query = """
    CREATE TABLE IF NOT EXISTS logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        date DATETIME DEFAULT CURRENT_TIMESTAMP,
        title TEXT NOT NULL,
        description TEXT,
        type TEXT,
        links TEXT,
        tags TEXT
    );
    """
    db.execute(query)


def create_log(db, user_id: int, payload: LogCreate) -> int:
    query = """
    INSERT INTO logs (user_id, title, description, type, links, tags)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor = db.execute(
        query,
        (
            user_id,
            payload.title,
            payload.description,
            payload.type,
            payload.links,
            payload.tags,
        )
    )
    return cursor.lastrowid



def remove_log(db, user_id: int, log_id: int) -> bool:
    query = """
    DELETE FROM logs
    WHERE log_id = ? AND user_id = ?
    """
    cursor = db.execute(query, (log_id, user_id))
    return cursor.rowcount > 0



def get_logs_by_day(db, user_id: int, date: str = None):
    if date:
        print("Fetching logs for date:", date)
        query = """
        SELECT *
        FROM logs
        WHERE user_id = ?
          AND DATE(date) = DATE(?)
        ORDER BY date DESC
        """
        params = (user_id, date)
    else:
        query = """
        SELECT *
        FROM logs
        WHERE user_id = ?
          AND DATE(date) = DATE('now', 'localtime')
        ORDER BY date DESC
        """
        params = (user_id,)

    rows = db.fetchall(query, params)
    return [dict(row) for row in rows]

# SELECT * FROM logs WHERE user_id = 1 AND  DATE(date) = DATE("2026-01-19") ORDER BY date DESC