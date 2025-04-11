"""
coding:utf-8
@Software : PyCharm
@File : postgres_client.py
@Time : 2023/10/31 13:51
@Author : Ryan Gao
@Email : jiameng.jm.gao@deltaww.com
@description : 
"""
import psycopg2

from shared.base.config import PostgresSettings


class PyPostgresClient(object):
    def __init__(self):
        self.host = PostgresSettings.HOST
        self.port = PostgresSettings.PORT
        self.user = PostgresSettings.USER
        self.password = PostgresSettings.PASSWORD
        self.database = PostgresSettings.DB

        self.connection = None

    def connect(self):
        while not self.connection:
            try:
                self.connection = self._connect(self.database)
            except Exception as e:
                print(f"Error connecting to PostgreSQL: {e}")
                try:
                    self.create_database(self.database)
                except Exception as e:
                    print(e)

        print(f"Connected to PostgreSQL, database: {self.database}")

    def _connect(self, db_name='postgres'):
        conn = None
        while not conn:
            conn = psycopg2.connect(
                database=db_name,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
        conn.autocommit = True      # 自动提交事务
        return conn

    def create_database(self, new_db_name):
        auth_conn = self._connect()
        if auth_conn:
            try:
                with auth_conn.cursor() as cur:
                    cur.execute("CREATE DATABASE {new_db_name};".format(new_db_name=new_db_name))
                    print(f"Database '{new_db_name}' created successfully.")
                auth_conn.commit()  # Commit the transaction
            except Exception as e:
                print(f"Error creating database: {e}")
            finally:
                auth_conn.close()

    def execute_query(self, query):
        if not self.connection:
            print("Not connected to PostgreSQL")
            self.connect()
            return

        try:
            with self.connection.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
                return result
        except Exception as e:
            print(f"Error executing query: {e}")

    def insert_data(self, query, data):
        if not self.connection:
            print("Not connected to PostgreSQL")
            self.connect()
            return

        try:
            with self.connection.cursor() as cur:
                cur.execute(query, data)
        except Exception as e:
            print(f"Error inserting data: {e}")

    def insert_datas(self, query, datas):
        if not self.connection:
            print("Not connected to PostgreSQL")
            self.connect()
            return

        try:
            with self.connection.cursor() as cur:
                cur.executemany(query, datas)
        except Exception as e:
            print(f"Error inserting data: {e}")

    def close(self):
        if self.connection:
            self.connection.close()
            print(f"Connection to PostgreSQL closed: {self.database}")

    def __del__(self):
        self.close()
