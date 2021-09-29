import sqlite3

conn = sqlite3.connect("Database.db")

c = conn.cursor()

def create_table(name:str):
  with conn:
    c.execute("""CREATE TABLE IF NOT EXISTS {} (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        word TEXT
        )""".format(name))
    conn.commit()


def insert(table, column, thing):
  with conn:
      c.execute("INSERT INTO {} ({}) VALUES (:thing)".format(table, column), {'thing':thing})
      conn.commit()


def execute(cmd):
  with conn:
    c.execute(cmd)
    conn.commit()


def search(cmd):
  with conn:
    c.execute(cmd)
    conn.commit()
    return c.fetchall()


def undo():
  with conn:
    conn.rollback()