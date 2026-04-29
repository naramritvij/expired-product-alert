# config/db_config.py
# -------------------------------------------------------
# Database connection settings for Oracle
# In production, load these from environment variables
# or a .env file — never hardcode credentials in Git!
# -------------------------------------------------------

import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "user":     os.getenv("DB_USER",     "your_username"),
    "password": os.getenv("DB_PASSWORD", "your_password"),
    "dsn":      os.getenv("DB_DSN",      "localhost:1521/XEPDB1"),  # adjust for your Oracle instance
}
