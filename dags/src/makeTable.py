from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2


def make_database():
    """
    Make the Postgres database and create the table.
    """
    dbname = "airflow_db"
    username = "phunc20"
    tablename = "cwb_general"

    engine = create_engine(
        f'postgresql+psycopg2://{username}@localhost/{dbname}'
    )

    if not database_exists(engine.url):
        create_database(engine.url)

    conn = psycopg2.connect(database=dbname, user=username)

    cur = conn.cursor()

    create_table = (
        f"""CREATE TABLE IF NOT EXISTS {tablename}
        (
            city         TEXT,
            weather      TEXT,
            pop          REAL,
            min_temp     REAL,
            max_temp     REAL,
            todays_date  DATE
       )
       """
    )

    cur.execute(create_table)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    make_database()
