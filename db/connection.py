# db/connection.py
# -------------------------------------------------------
# Handles Oracle DB connection using cx_Oracle
# -------------------------------------------------------

import cx_Oracle
from config.db_config import DB_CONFIG


def get_connection():
    """Return a live Oracle DB connection."""
    try:
        conn = cx_Oracle.connect(
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            dsn=DB_CONFIG["dsn"]
        )
        return conn
    except cx_Oracle.DatabaseError as e:
        print(f"[ERROR] Could not connect to Oracle DB: {e}")
        raise
