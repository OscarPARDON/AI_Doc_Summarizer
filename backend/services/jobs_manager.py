import sqlite3

def create_job_table(cnx : sqlite3.Connection):
        """ Create table for jobs in the database """

        cursor = cnx.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS jobs (uuid TEXT PRIMARY KEY,status TEXT,result TEXT)"
        )
        cnx.commit()

def init_job(cnx : sqlite3.Connection, uuid : str, filename : str, status : str ):
        """ Create a new job entry in the database """
        cursor = cnx.cursor()
        cursor.execute(
            "INSERT INTO jobs (uuid, filename, status) VALUES (?, ?, ?)",
            (uuid, filename, status),
        )
        cnx.commit()

def update_job(cnx : sqlite3.Connection, uuid : str, status : str, result : str):
        """ Update an existing job entry in the database """
        cursor = cnx.cursor()
        cursor.execute("UPDATE jobs SET status=?, result=? WHERE uuid=?", (status,result, uuid))
        cnx.commit()

def get_job(cnx : sqlite3.Connection, uuid : str):
        """ Return the job with the given uuid """
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM jobs WHERE uuid=?", (uuid,))
        return cursor.fetchone()

def delete_job(cnx : sqlite3.Connection, uuid : str):
        """ Delete the job with the given uuid """
        cursor = cnx.cursor()
        cursor.execute("DELETE FROM jobs WHERE uuid=?", (uuid,))
        cnx.commit()