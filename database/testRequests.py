import sqlite3

def createTest(test_file:str, file_type:str, count_question:int, answers:str, published:str):
    try:
        with sqlite3.connect("database.db") as db:
            cursor = db.cursor()
            cursor.execute("""
    INSERT INTO test (test_file, file_type, count_question, answers, published)
    VALUES (?, ?, ?, ?, ? )
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
        with sqlite3.connect("database.db") as db:
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
        with sqlite3.connect("database.db") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute("""
    SELECT * FROM test WHERE id = ?
""", (test_id, ))
            test = cursor.fetchone()
            return dict(test) if test else False
    except Exception as e:
        print("Testni olishda hatolik mavjud. ", e)
        return False
    
def getAllAllTest():
    try:   
        with sqlite3.connect("database.db") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute("""
    SELECT * FROM test
""", )
            test = cursor.fetchone()
            return [dict(test) if test else False]
    except Exception as e:
        print("Testni olishda hatolik mavjud. ", e)
        return False
    
def updateTestHolat(test_id: int, published:str):
    try:   
        with sqlite3.connect("database.db") as db:
            cursor = db.cursor()
            cursor.execute("""
    UPDATE test SET published = ?  WHERE id = ?
""", (published, test_id, ))
            db.commit()
            return True
    except Exception as e:
        print("Testni olishda hatolik mavjud. ", e)
        return False
    

def updateTest(test_id: int, count_question: int, answers: str):
    try:
        with sqlite3.connect("database.db") as db:
            cursor = db.cursor()
            cursor.execute("""
                UPDATE test 
                SET count_question = ?, answers = ?
                WHERE id = ?
            """, (count_question, answers, test_id))
            db.commit()
            return True
    except Exception as e:
        print("Testni o'zgartirishda hatolik mavjud:", e)
        return False

def deleteTest(test_id:int):
    try:   
        with sqlite3.connect("database.db") as db:
            cursor = db.cursor()
            cursor.execute("""
    DELETE FROM test  WHERE id = ?
""", ( test_id,  ))
            db.commit()
            return True
    except Exception as e:
        print("Testni o'chirishda hatolik mavjud. ", e)
        return False