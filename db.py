import sqlite3
import _osx_support
import os
from datetime import date


class Database:
    def __init__(self, path):
        # Initializing important vars
        self.path = path
        self.conn = sqlite3.connect(os.path.join(self.path, 'sem.db'))
        self.curr = self.conn.cursor()
        try:
            # Creating tables for reval and reg because they have different formats
            self.curr.execute('''
                CREATE TABLE IF NOT EXISTS reg(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usn varchar(20) NOT NULL,
                    name varchar(200) NOT NULL,
                    sem int NOT NULL, 
                    sub_code varchar(200) NOT NULL,
                    sub_name text NOT NULL,
                    internal int NOT NULL,
                    external int NOT NULL,
                    total int NOT NULL,
                    result varchar(3) NOT NULL,
                    announced date,
                    date date);
            ''')
            self.curr.execute('''
                CREATE TABLE IF NOT EXISTS rev(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usn varchar(20) NOT NULL,
                    name varchar(200) NOT NULL,
                    sem int NOT NULL, 
                    sub_code varchar(200) NOT NULL, 
                    sub_name text NOT NULL,
                    internal int NOT NULL,
                    old_m int NOT NULL,
                    old_res varchar(3) NOT NULL,
                    rv_m int NOT NULL,
                    rv_res varchar(3) NOT NULL,
                    final_m int NOT NULL,
                    final_res varchar(3) NOT NULL,
                    date date NOT NULL);
''')
            self.conn.commit()
        except:
            print("An error occured with DB initialization!")

    def insertRecord(self, reval, usn, name, sem, *args):
        try:
            # Making data tuple with *args to make a common insert function
            data = (usn, name, sem, *args, date.today())
            if not reval:
                self.curr.execute('''
                INSERT INTO reg(
                    usn,
                    name, 
                    sem, 
                    sub_code, 
                    sub_name, 
                    internal, 
                    external, 
                    total, 
                    result, 
                    announced, 
                    date) 
                    values(?,?,?,?,?,?,?,?,?,?,?);
                ''', data)
                self.conn.commit()
            else:
                self.curr.execute('''
                INSERT INTO rev(
                    usn,
                    name,
                    sem, 
                    sub_code,
                    sub_name,
                    internal,
                    old_m,
                    old_res,
                    rv_m,
                    rv_res,
                    final_m,
                    final_res,
                    date
                ) values(?,?,?,?,?,?,?,?,?,?,?,?,?)
                ''', data)
        except Exception as e:
            print(f"Error occured with inserting record! {e}")

    def __del__(self):
        try:
            # Destructor will close db
            self.conn.close()
        except:
            print("Error occured closing DB!")
