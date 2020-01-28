import hashlib
from database import DB

from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature,
    SignatureExpired
    )

SECRET_KEY = 'ssadkfvnklasf@13AS|asdganaofASFANSKF334'


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
            db.execute(
                '''
                    INSERT INTO users
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', values
            )

            return self

    @staticmethod
    def get_user_by_email(email):
        if not email:
            return None
        with DB() as db:
            row = db.execute(
                '''
                    SELECT email, name, address, phone FROM users
                    WHERE email = ?
                ''', (email,)
            ).fetchone()
            if row:
                return User(*row)
            return False

    @staticmethod
    def encrypt_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def verify_password(self, password, email):
        with DB() as db:
            passw = db.execute(
                '''
                    SELECT password FROM users
                    WHERE email = ?
                ''', (email,)
            ).fetchone()
        return passw[0] ==\
            hashlib.sha256(password.encode('utf-8')).hexdigest()

    def delete(self):
        with DB() as db:
            db.execute(
                '''
                    DELETE FROM users
                    WHERE name = ?
                ''', (self.name,)
            )

            return self

    def generate_token(self):
        s = Serializer(SECRET_KEY, expires_in=600)
        return s.dumps({'email': self.email})

    @staticmethod
    def verify_token(token):
        s = Serializer(SECRET_KEY)
        try:
            s.loads(token)
        except SignatureExpired:
            return False
        except BadSignature:
            return False
        return True
