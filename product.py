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
        self.owner_id = None
        self.publisher_id = None

        self.values = (self.id, self.title, self.content, self.price,
                       self.published, self.is_active)

    @staticmethod
    def get_current_datetime():
        now = datetime.now()

        return now.strftime("%d-%m-%Y %H:%M:%S")

    def get_product_published_date(self):
        with DB() as db:
            return db.execute(
                '''
                    SELECT published
                    FROM products
                    WHERE id = ?
                ''', (self.id,)
            ).fetchone()[0]

    def get_publisher_id(self):
        with DB() as db:
            return db.execute(
                '''
                    SELECT publisher_id
                    FROM products
                    WHERE id = ?
                ''', (self.id,)
            ).fetchone()[0]

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

    def add_product(self, publisher_id):
        with DB() as db:
            self.values += (publisher_id, publisher_id)

            db.execute(
                '''
                    INSERT INTO products (id, title, content, price,
                        published, is_active, owner_id, publisher_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
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
            all_values = (new.title, new.content, new.price, self.id)

            db.execute(
                '''
                    UPDATE products
                    SET title = ?,
                        content = ?,
                        price = ?
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

    @staticmethod
    def buy_product(product_id, owner_id):
        with DB() as db:
            db.execute(
                '''
                    UPDATE products
                    SET is_active = 0,
                        owner_id = ?
                    WHERE id = ?
                ''', (owner_id, product_id)
            )

    @staticmethod
    def get_username_by_publisher_id(product_title):
        with DB() as db:
            return db.execute(
                '''
                    SELECT users.id, products.publisher_id,
                        users.name, products.title
                    FROM users
                    INNER JOIN products
                        ON users.id = products.publisher_id
                            AND products.title = ?
                ''', (product_title,)
            ).fetchone()[2]
