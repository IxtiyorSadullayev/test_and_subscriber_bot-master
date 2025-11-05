import sqlite3

def createTest(test_file:str, file_type:str, count_question:str, answers:str, published:str):
    try:
        with sqlite3.connect("mukam_bot.db") as db:
            cursor = db.cursor()
            cursor.execute("""
    INSERT INTO test (test_file, file_type, count_question, answers, published)
    VALUES (?, ?, ?, ?, ?, ?)
""", (test_file, file_type, count_question, answers, published, ))
            db.commit()
            return True
    except Exception as e:
        print("Test yaratishda hatolik mavjud: ", e)
        return False

# published
# Jarayonda
# Active
# Tugallangan
def getTestToAdmin(published:str):
    try:
        with sqlite3.connect("mukam_bot.db") as db:
            db.row_factory = sqlite3.Row 
            cursor = db.cursor()
            cursor.execute("""
    SELECT * FROM test WHERE published = ?
""", (published, ))
            test = cursor.fetchall()
            return [dict(row) for row in test] if test else []
    except Exception as e:
        print("Testni olishda hatolik mavjud. ", e)
        return False


def getTestById(test_id):
    try:   
        with sqlite3.connect("mukam_bot.db") as db:
            cursor = db.cursor()
            cursor.execute("""
    SELECT * FROM test WHERE id = ?
""", (test_id, ))
            test = cursor.fetchone()
            return dict(test) if test else False
    except Exception as e:
        print("Testni olishda hatolik mavjud. ", e)
        return False