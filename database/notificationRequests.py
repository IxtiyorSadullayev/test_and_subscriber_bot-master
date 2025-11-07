import sqlite3


def createNotification(tg_id: int, test_id: int, tanlov_id: int, holat: str):
    try:
        with sqlite3.connect("mukam_bot.db") as db:
            cursor = db.cursor()
            cursor.execute("""
    INSERT INTO notification (tg_id, test_id, tanlov_id, holat)
    VALUES (?, ?, ?, ?)
""", (tg_id, test_id, tanlov_id, holat, ))
            db.commit()
            return True
    except Exception as e:
        print("Notifikation yaratishda hatolik mavjud", e)
        return False

def getTestNotifications(test_id: int):
    try: 
        with sqlite3.connect("mukam_bot.db") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute("""
    SELECT n.id, u.fullname, u.phoneNumber, n.holat FROM notification n 
    JOIN user u ON n.tg_id = u.tg_id
    WHERE n.test_id = ? 
""", (test_id,))
            data = cursor.fetchall()
            return [dict(row) for row in data] 
    except Exception as e:
        print("Ma'lumotlarni olishda hatolik mavjud. ", e)
        return False
    
def getTanlovNotifications(tanlov_id: int):
    try: 
        with sqlite3.connect("mukam_bot.db") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute("""
    SELECT n.id, u.fullname, u.phoneNumber, n.holat FROM notification n 
    JOIN user u ON n.tg_id = u.tg_id
    WHERE n.tanlov_id = ? 
""", (tanlov_id,))
            data = cursor.fetchall()
            return [dict(row) for row in data] 
    except Exception as e:
        print("Ma'lumotlarni olishda hatolik mavjud. ", e)
        return False
