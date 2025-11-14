import sqlite3


def createChaqirData(tg_id: int, client_id: int):
    try:
        with sqlite3.connect("mukam_bot.db") as db:
            cursor = db.cursor()
            cursor.execute("""
    INSERT INTO chaqiruv (tg_id, client_id)
    VALUES (?, ?)
""", (tg_id, client_id, ))
            db.commit()
            return True
    except Exception as e:
        print("Chaqiruv jadvaliga ma'lumot kiritishda hatolik mavjud.", e)
        return False

def getForUserData(tg_id: int):
    try:
        with sqlite3.connect("mukam_bot.db") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute("""
    SELECT * FROM chaqiruv WHERE tg_id = ?
""", (tg_id, ))
            data = cursor.fetchall()
            return len(data)
    except Exception as e:
        print("Chaqiruv jadvalidagi ma'lumotlarni olishda hatolik mavjud.", e)
        return False