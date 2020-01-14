from database import DB


class Product:
    def __init__(self, id, title, content, price, published,
                 is_active, publisher_id, owner_id=None):
        self.id = id
        self.title = title
        self.content = content
        self.price = price
        self.published = published
        self.is_active = is_active
        self.owner_id = owner_id
        self.publisher_id = publisher_id

        self.values = (self.title, self.content, self.price,
                       self.published, self.is_active,
                       self.owner_id, self.publisher_id)

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
                    SELECT *
                    FROM products
                '''
            ).fetchall()

            return [Product(*product) for product in products]

    @staticmethod
    def get_all_active_products():
        with DB() as db:
            products = db.execute(
                '''
                    SELECT *
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
                    SELECT *
                    FROM products
                    WHERE is_active = 0
                '''
            ).fetchall()

            return [Product(*product) for product in products]

    @staticmethod
    def get_all_user_products(user_id):
        with DB() as db:
            products = db.execute(
                '''
                    SELECT *
                    FROM products
                    WHERE id = ?
                ''', (user_id,)
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
                        published = ?,
                        is_active = ?
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

    def buy_product(self, owner_id):
        with DB() as db:
            db.execute(
                '''
                    UPDATE products
                    SET owner_id = ?
                        is_active = ?
                ''', (owner_id, 0)
            )
