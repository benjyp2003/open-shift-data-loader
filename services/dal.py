from mysql.connector import Error
import mysql.connector
import os

class Dal:

    def __init__(self):
        # Connection configuration
        self.conn_config = {
            'host': os.getenv('MYSQL_HOST', 'mysql'),
            'user': os.getenv('MYSQL_USER', 'root'),
            'password': os.getenv('MYSQL_PASSWORD', 'pwd'),
            'database': os.getenv('MYSQL_DATABASE', ''),
            'autocommit': False,
            'charset': 'utf8mb4'
        }

    def get_connection(self):
        try:
            return mysql.connector.connect(**self.conn_config)
        except Error as e:
            print("Error connecting to MySQL:", e)
            raise

    def execute(self, query, params=None, commit=False, dictionary=False):
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=dictionary)
            
            cursor.execute(query, params or ())
            print("Query executed successfully.")

            if commit:
                conn.commit()
                print("Changes committed to database.")
            
            return cursor

        except Error as e:
            print("Database execution error:", e)
            if conn and commit:
                conn.rollback()
                print("Transaction rolled back.")
            raise
        finally:
            if conn:
                conn.close()

    def fetch_all(self, query, params=None):
        try:
            cursor = self.execute(query, params, dictionary=True)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            print("Error fetching all rows:", e)
            return []

    def fetch_one(self, query, params=None):
        try:
            cursor = self.execute(query, params, dictionary=True)
            result = cursor.fetchone()
            cursor.close()
            return result
        except Error as e:
            print("Error fetching one row:", e)
            return None

    def execute_many(self, query, params_list, commit=True):
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.executemany(query, params_list)
            print(f"Executed {len(params_list)} queries successfully.")

            if commit:
                conn.commit()
                print("All changes committed to database.")
            
            return cursor

        except Error as e:
            print("Database execution error:", e)
            if conn and commit:
                conn.rollback()
                print("Transaction rolled back.")
            raise
        finally:
            if conn:
                conn.close()
