import sqlite3
from datetime import date


class Database:
    def __init__(self, name):
        self._conn = sqlite3.connect(name)
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()

    def insert_or_ignore_into_products_table(self, product_list):
        products = [{"product": product.name} for product in product_list]
        self.cursor.executemany("""
        INSERT OR IGNORE INTO products (Product) 
        VALUES (:product)
        """, products)

    def insert_into_prices_table(self, product_list):
        products = [{"price": product.price, "vendor": product.vendor, "product": product.name, "date": date.today()}
                    for product in product_list]
        self.cursor.executemany("""
        INSERT INTO prices (ProductID, VendorID, Product, Price, Date) 
        VALUES 
        ((SELECT ID from products WHERE Product=:product), 
        (SELECT ID from vendors WHERE Vendor=:vendor), 
        :product, 
        :price, 
        :date)"""
                                , products)