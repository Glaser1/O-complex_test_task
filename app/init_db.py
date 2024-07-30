import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()
DB_NAME = os.getenv("DB_NAME")


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """ 
    CREATE TABLE "user_search" (
        "id"	INTEGER,
        "user_id"	TEXT NOT NULL,
        "city"	TEXT NOT NULL,
        "requested_at"	DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY("id")
    );
    """
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
