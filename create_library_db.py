import sys, os, csv
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))

def open_source(file):
    with open(f, "r", encoding="utf-8") as f:
        csvreader = csv.reader(f)
        fields = next(csvreader)
        print(fields)
        for row in csvreader:
            print(row)
            # insert data to database
            insert_data(fields, row)

def create_connection():
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(f"{script_directory}/library.db")

    if not db.open():
        QMessageBox.critical(None, "Database Error", db.lastError().text())
        return False
    return True

def create_book_table():
    query = QSqlQuery()
    query.exec("""DROP TBALE IF EXISTS book""")
    query.exec("""CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    isbn13 INTEGER NOT NULL,
                    isbn10 TEXT NOT NULL,
                    title TEXT NOT NULL,
                    subtitle TEXT NOT NULL,
                    authors TEXT NOT NULL,
                    categories TEXT NOT NULL,
                    thumbnail TEXT NOT NULL,
                    description TEXT NOT NULL,
                    published_year INTEGER NOT NULL,
                    average_rating INTEGER NOT NULL,
                    num_pages INTEGER NOT NULL,
                    ratings_count INTEGER NOT NULL)""")
    
def create_user_table():
    query = QSqlQuery()
    query.exec("""DROP TBALE IF EXISTS users""")
    query.exec("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    name INTEGER NOT NULL,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT,
                    birth_date TEXT,
                    authorization TEXT NOT NULL)""")

def insert_data(fields, values):
    query = QSqlQuery()
    query.prepare(f"INSERT INTO books ({', '.join(fields)}) VALUES ({", ".join("?" for _ in range(len(values)))})")
    for value in values:
        query.addBindValue(value)

    if query.exec():
        print("Book inserted successfully!")
    else:
        print("Error inserting book:", query.lastError().text())


app = QApplication([])
if create_connection():
    print("Database connected successfully!")
    create_user_table()
    open_source(f"{script_directory}/assets/users.csv")
    create_book_table()
    open_source(f"{script_directory}/assets/books_dataset/data.csv")

    sys.exit()

app.exec()
