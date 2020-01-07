from database import DB
import hashlib


class User:
    def __init__(self, email, name, address, phone):
        self.id = None
        self.email = email
        self.password = None
        self.name = name
        self.address = address
        self.phone = phone

    def create(self, password):
        with DB() as db:
            values = (None, self.name, password, self.email,
                      self.address, self.phone)

            db.execute('''
                INSERT INTO users
                VALUES (?, ?, ?, ?, ?, ?)
                ''', values)

            return self

    @staticmethod
    def get_user_by_email(email):
        if not email:
            return None

        with DB() as db:
            row = db.execute('''
                SELECT * FROM users WHERE email = (?)''',
                             (email,)).fetchone()
            return User(*row)

    @staticmethod
    def encrypt_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def veryfy_password(self, password):
        return self.password == hashlib.sha256(password.encode('utf-8'))\
                                                .hexdigest()

    def delete(self):
        with DB() as db:
            db.execute("DELETE FROM users WHERE name = (?)", (self.name,))
            return self
