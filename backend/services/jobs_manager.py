import sqlite3


def create_job_table(cnx):
        cursor = cnx.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS jobs (uuid TEXT PRIMARY KEY,status TEXT,result TEXT)"
        )
        cnx.commit()

def init_job(cnx, uuid : str, status : str ):
        cursor = cnx.cursor()
        cursor.execute(
            "INSERT INTO jobs (uuid, status) VALUES (?, ?)",
            (uuid, status)
        )
        cnx.commit()

def update_job(cnx, uuid : str, status : str, result : str):
        cursor = cnx.cursor()
        cursor.execute("UPDATE jobs SET status=?, result=? WHERE uuid=?", (status,result, uuid))
        cnx.commit()

def get_job(cnx, uuid : str):
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM jobs WHERE uuid=?", (uuid,))
        return cursor.fetchone()

def delete_job(cnx, uuid : str):
        cursor = cnx.cursor()
        cursor.execute("DELETE FROM jobs WHERE uuid=?", (uuid,))
        cnx.commit()