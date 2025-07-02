import psycopg2

def init_db(app):
    app.db = psycopg2.connect(
        host="localhost",
        user="flaskapp",
        password="flaskapp",
        dbname="flaskappdb"
    )
    app.cursor = app.db.cursor()

    app.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            password VARCHAR(100)
        )
    """)
    app.db.commit()
