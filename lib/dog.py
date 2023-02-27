import sqlite3
# import pdb; pdb.set_trace()

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self,name,breed):
        self.id = None
        self.name = name
        self.breed = breed
    
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()
    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """
            INSERT INTO dogs (name,breed)
            VALUES (?,?)
        """
        CURSOR.execute(sql,(self.name,self.breed))
        CONN.commit()
        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]

    @classmethod
    def create(cls,name,breed):
        dog = Dog(name,breed)
        dog.save()
        return dog
    
    @classmethod
    def new_from_db(cls,row):
        dog = Dog(row[1],row[2])
        dog.id = row[0]
        return dog
    
    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM dogs"
        results = CURSOR.execute(sql)
        doglist = []
        for row in results:
            dog = Dog(row[1],row[2])
            dog.id = row[0]
            doglist.append(dog)
        return doglist
    @classmethod
    def find_by_name(cls,name):
        sql = "SELECT * FROM dogs WHERE name = ?"
        dogrow = CURSOR.execute(sql,(name,)).fetchone()
        if dogrow:
            dog = cls.new_from_db(dogrow)
            return dog
    @classmethod
    def find_by_id(cls,id):
        sql = "SELECT * FROM dogs WHERE id = ?"
        dogrow = CURSOR.execute(sql,(id,)).fetchone()
        dog = cls.new_from_db(dogrow)
        return dog
    @classmethod
    def find_or_create_by(cls,name,breed):
        sql = "SELECT * FROM dogs WHERE name = ? AND breed = ?"
        result = CURSOR.execute(sql,(name,breed)).fetchone()
        if not result:
            return cls.create(name,breed)
    def update(self):
        sql = """UPDATE dogs SET name = ? WHERE id = ?"""
        CURSOR.execute(sql,(self.name,self.id))
        CONN.commit()

