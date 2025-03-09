import sqlite3, os, sys
script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))

conn = sqlite3.connect(f"{script_directory}/library.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("Tables in database:", tables)

cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
print("Users table content:", rows)

conn.close()
