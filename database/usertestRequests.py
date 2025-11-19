import sqlite3

def createuserTest(tg_id: int, test_id: int, answers: str, score: int, result:str):
    try:
        with sqlite3.connect("database.db") as db:
            cursor = db.cursor()
            cursor.execute("""
    INSERT INTO usertest (tg_id, test_id, answers, score, result)
    VALUES (?, ?, ?, ?, ?) 
""", (tg_id, test_id, answers, score, result))
            db.commit()
            return True
    except Exception as e:
        print("User testini kiritish jarayonida hatolik mavjud, ", e)
        return False


def getUserTesttoAdmin(test_id):
    try:
        with sqlite3.connect("database.db") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute("""
            SELECT tu.id, u.fullname, u.phoneNumber, tu.test_id, tu.answers, tu.result, tu.score, tu.created  FROM usertest as tu
            JOIN user as u ON tu.tg_id = u.tg_id
            WHERE tu.test_id = ?""", (test_id, ))
            testlar = cursor.fetchall()
            return [dict(row) for row in testlar] if testlar else []
    except Exception as e:
        print("testlarni admin sifatida ko'rishda hatolik mavjud, ", e)
        return False

def getUserTesttoUserTest(tg_id):
    try:
        with sqlite3.connect("database.db") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute("SELECT * FROM usertest WHERE tg_id = ?", (tg_id, ))
            testlar = cursor.fetchall()
            return [dict(row) for row in testlar] if testlar else []
    except Exception as e:
        print("testlarni foydalanuvchi sifatida ko'rishda hatolik mavjud, ", e)
        return False

def getTekshiruvTestUser(tg_id:int, test_id:int):
    try:
        with sqlite3.connect("database.db") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute("SELECT * FROM usertest WHERE tg_id = ? AND test_id = ?", (tg_id,test_id, ))
            testlar = cursor.fetchall()
            if len(testlar)>0:
                return False
            return True
    except Exception as e:
        print("testlarni foydalanuvchi sifatida ko'rishda hatolik mavjud, ", e)
        return False
def getAllAlluserTestUser():
    try:
        with sqlite3.connect("database.db") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute("SELECT * FROM usertest ",)
            testlar = cursor.fetchall()
            return [dict(row) for row in testlar]
    except Exception as e:
        print("testlarni foydalanuvchi sifatida ko'rishda hatolik mavjud, ", e)
        return False
