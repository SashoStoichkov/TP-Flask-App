from datetime import datetime

from database import DB


class Product:
    def __init__(self, id, title, content, price):
        self.id = id
        self.title = title
        self.content = content
        self.price = price
        self.published = self.get_current_datetime()
        self.is_active = 1
        self.owner_id = 1  # TODO
        self.publisher_id = 1  # TODO

        self.values = (self.title, self.content, self.price,
                       self.published, self.is_active,
                       self.owner_id, self.publisher_id)

    @staticmethod
    def get_current_datetime():
        now = datetime.now()

        return now.strftime("%d-%m-%Y %H:%M:%S")

    @staticmethod
    def find_product(id):
        with DB() as db:
            product = db.execute(
                '''
                    SELECT id, title, content, price
                    FROM products
                    WHERE id = ?
                ''', (id,)
            ).fetchone()

            return Product(*product)

    def add_product(self):
        with DB() as db:
            db.execute(
                '''
                    INSERT INTO products (title, content, price,
                        published, is_active, owner_id, publisher_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', self.values
            )

            return self

    @staticmethod
    def get_all_products():
        with DB() as db:
            products = db.execute(
                '''
                    SELECT id, title, content, price
                    FROM products
                '''
            ).fetchall()

            return [Product(*product) for product in products]

    @staticmethod
    def get_all_active_products():
        with DB() as db:
            products = db.execute(
                '''
                    SELECT id, title, content, price
                    FROM products
                    WHERE is_active = 1
                '''
            ).fetchall()

            return [Product(*product) for product in products]

    @staticmethod
    def get_all_unactive_products():
        with DB() as db:
            products = db.execute(
                '''
                    SELECT id, title, content, price
                    FROM products
                    WHERE is_active = 0
                '''
            ).fetchall()

            return [Product(*product) for product in products]

    def edit_product(self, new):
        with DB() as db:
            all_values = new.values + (self.id,)

            db.execute(
                '''
                    UPDATE products
                    SET title = ?,
                        content = ?,
                        price = ?,
                        is_active = ?,
                        owner_id = ?
                    WHERE id = ?
                ''', all_values
            )

            return self

    def delete_product(self):
        with DB() as db:
            db.execute(
                '''
                    DELETE
                    FROM products
                    WHERE id = ?
                ''', (self.id,)
            )
