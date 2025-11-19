import sqlite3

def createUser(fullname:str, username:str, phoneNumber:str, tg_id:int, usernick=None, role='USER'):
    try:
        with sqlite3.connect("database.db") as db:
            cursor = db.cursor()
            cursor.execute("""
            INSERT INTO user (fullname, username, phoneNumber, tg_id, usernick, role)
            VALUES (?,?,?,?,?,?)
        """, (fullname, username, phoneNumber, tg_id, usernick, role,))
            db.commit()
        return True
    except Exception as e:
        print("User yaratishda hatolik", e)
        return False
    # User yaratish oynasi.

def getAllUsers():
    try:
        with sqlite3.connect("database.db") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute("""
    SELECT id, tg_id FROM user WHERE role = 'USER'
""")
            data = cursor.fetchall()
            return [dict(row) for row in data]
    except Exception as e:
        print("Barcha userlanri olishda hatolik mavjud", e)
        return False

def getAllAllUsers():
    try:
        with sqlite3.connect("database.db") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute("""
    SELECT * FROM user 
""")
            data = cursor.fetchall()
            return [dict(row) for row in data]
    except Exception as e:
        print("Barcha userlanri olishda hatolik mavjud", e)
        return False

def getUserByTg_id(tg_id: int):
    # Userni qidirib topish id orqali
    try:
        with sqlite3.connect("database.db") as db:
            db.row_factory=sqlite3.Row
            cursor = db.cursor()
            user = cursor.execute("""
    SELECT * FROM user WHERE tg_id = ? 
""", (tg_id, ))
            return dict(user.fetchone()) if user else False
    except Exception as e:
        print("Userni olishda hatolik mavjud.: ", e)
        return False


def updateUserByTg_id_role(tg_id: int, role:str):
    try:
        with sqlite3.connect("database.db") as db:
            cursor = db.cursor()
            cursor.execute("""
    UPDATE user SET role = ? WHERE tg_id = ?
""", (role, tg_id,))
            db.commit()
            if cursor.rowcount == 0:
                print("Bunday tg_id topilmadi.")
                return False
        return True
    except Exception as e:
        print("Userni roleni yangilashda hatolik yuzaga keldi", e)
        return False

def updateUserByTg_id_fullname(tg_id: int, fullname:str):
    try:
        with sqlite3.connect("database.db") as db:
            cursor = db.cursor()
            cursor.execute("""
    UPDATE user SET fullname = ? WHERE tg_id = ?
""", (fullname, tg_id,))
            db.commit()
            if cursor.rowcount == 0:
                print("Bunday tg_id topilmadi.")
                return False
        return True
    except Exception as e:
        print("Userni fullnameini yangilashda hatolik yuzaga keldi", e)
        return False

def updateUserByTg_id_phoneNumber(tg_id: int, phoneNumber:str):
    try:
        with sqlite3.connect("database.db") as db:
            cursor = db.cursor()
            cursor.execute("""
    UPDATE user SET phoneNumber = ? WHERE tg_id = ?
""", (phoneNumber, tg_id,))
            db.commit()
            if cursor.rowcount == 0:
                print("Bunday tg_id topilmadi.")
                return False
        return True
    except Exception as e:
        print("Userni phoneNumberini yangilashda hatolik yuzaga keldi", e)
        return False