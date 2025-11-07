import sqlite3 

def createUser_table():
    db = sqlite3.connect("mukam_bot.db")
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT NOT NULL,
        username TEXT,
        phoneNumber TEXT NOT NULL,
        tg_id INTEGER NOT NULL,
        usernick TEXT,
        role TEXT DEFAULT 'USER'
    )
    """)
    db.commit()
    db.close()

def createTanlov():
    db = sqlite3.connect("mukam_bot.db")
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tanlov(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        image TEXT NOT NULL,
        started_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        published TEXT DEFAULT 'JARAYONDA'

    )
    """)
    db.commit()
    db.close()


def createTest():
    db = sqlite3.connect("mukam_bot.db")
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS test(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        test_file TEXT NOT NULL,
        file_type TEXT NOT NULL,
        count_question INTEGER NOT NULL,
        answers TEXT NOT NULL,
        published TEXT DEFAULT 'JARAYONDA'
    )
    """)
    db.commit()
    db.close()

def createUserTest():
    db = sqlite3.connect("mukam_bot.db")
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usertest(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        test_id INTEGER NOT NULL,
        answers TEXT NOT NULL,
        score INTEGER NOT NULL,
        result TEXT NOT NULL
    )
    """)
    db.commit()
    db.close() 

def createNotification():
    db = sqlite3.connect("mukam_bot.db")
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notification(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tg_id INTEGER NOT NULL,
    test_id INTEGER NULL,
    tanlov_id INTEGER NULL,
    holat TEXT NOT NULL
    )
""") 