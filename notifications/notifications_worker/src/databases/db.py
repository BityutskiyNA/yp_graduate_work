import psycopg2
from worker.config import Postgres

conn = psycopg2.connect(
    host=Postgres.host,
    port=Postgres.port,
    database=Postgres.db,
    user=Postgres.user,
    password=Postgres.password
)


def pg_create(message, status):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            messages JSON,
            status VARCHAR NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    data = (message, status)
    cur.execute("INSERT INTO messages (messages, status) VALUES (%s, %s)", data)

    conn.commit()

    cur.close()
