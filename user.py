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
            passwd = db.execute(
                '''
                    SELECT password FROM users
                    WHERE email = ?
                ''', (email,)
            ).fetchone()[0]

        return passwd ==\
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

    @staticmethod
    def get_id_by_email(email):
        with DB() as db:
            return db.execute(
                '''
                    SELECT id FROM users
                    WHERE email = ?
                ''', (email,)
            ).fetchone()[0]

    @staticmethod
    def get_username_by_id(id):
        with DB() as db:
            return db.execute(
                '''
                    SELECT name FROM users
                    WHERE id = ?
                ''', (id,)
            ).fetchone()[0]

    # TODO: fix this
    # def get_all_products_bought(self):
    #     with DB() as db:
    #         products = db.execute(
    #             '''
    #                 SELECT *
    #                 FROM products
    #                 WHERE owner_id != publisher_id
    #                     AND owner_id = ?
    #             ''', (self.id,)
    #         ).fetchall()

    #         return [product for product in products]