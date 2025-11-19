import sqlite3


"""
published
JARAYONDA
AMALDA
TUGADI
"""

def createTanlovDb(name:str, description:str, image:str, started_date:str, end_date:str, published:str):
    try:
        with sqlite3.connect("database.db") as db:
            cursor = db.cursor()
            cursor.execute("""
    INSERT INTO tanlov (name, description, image, started_date, end_date, published)
    VALUES (?, ?, ?, ?, ?, ?)
""", (name, description, image, started_date, end_date, published, ))
            db.commit()
            return True
    except Exception as e:
        print("Tanlov yaratishda hatolik mavjud: ", e)
        return False


def getAllTanlov():
    try:
        with sqlite3.connect("database.db") as db:
            db.row_factory = sqlite3.Row  
            cursor = db.cursor()
            cursor.execute("SELECT * FROM tanlov")
            tanlovlar = cursor.fetchall()
            
            return [dict(row) for row in tanlovlar] if tanlovlar else []
    except Exception as e:
        print("Tanlovlarni olishda hatolik mavjud:", e)
        return False


def getTanlovlar(published: str):
    try:
        with sqlite3.connect("database.db") as db:
            db.row_factory = sqlite3.Row  
            cursor = db.cursor()
            cursor.execute("SELECT * FROM tanlov WHERE published = ?", (published, ))
            tanlovlar = cursor.fetchall()
            
            return [dict(row) for row in tanlovlar] if tanlovlar else []
    except Exception as e:
        print("Tanlovlarni olishda hatolik mavjud:", e)
        return False

def getOneTanlov(tanlov_id: int):
    try:
        with sqlite3.connect("database.db") as db:
            db.row_factory = sqlite3.Row 
            cursor = db.cursor()
            tanlov = cursor.execute("SELECT * FROM tanlov WHERE id = ?", (tanlov_id,)).fetchone()
            return dict(tanlov) if tanlov else False
    except Exception as e:
        print("Bitta tanlovni olishda hatolik mavjud, ", e)
        return False
    
def updateTanlovHolati(tanlov_id: int, published:str):
    try:
        with sqlite3.connect("database.db") as db:
            cursor = db.cursor()
            cursor.execute("UPDATE tanlov SET published = ? WHERE id = ?", (published, tanlov_id,))
            db.commit()
            return True
    except Exception as e:
        print("Bitta tanlovni olishda hatolik mavjud, ", e)
        return False
    