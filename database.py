import sqlite3
from datetime import date, datetime


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

    def insert_product_into_products_table_if_new(self, product_list):
        products = [{"product": product.product_name,
                     "url": product.product_url}
                    for product in product_list]
        self.cursor.executemany("""
        INSERT OR IGNORE INTO products (Product, ProductURL) 
        VALUES (:product, :url)
        """, products)

    def insert_price_into_prices_table_if_changed(self, product_list):
        today = int(datetime.combine(date.today(), datetime.min.time()).timestamp())

        product_list = [{"price": product.price,
                         "vendor": product.vendor,
                         "product": product.product_name,
                         "date": today}
                        for product in product_list]
        # date is repeated for each product, can refactor? Would need to change execute lines

        # The full statement after this only works if the product has an existing price in the prices table
        # This statement performs the initial insert if required
        # Potential to make this cleaner?
        self.cursor.executemany("""
                        INSERT OR IGNORE INTO prices (ProductID, VendorID, Price, Date)
                        SELECT
                               (SELECT ID FROM products WHERE Product = :product),
                               (SELECT ID FROM vendors WHERE Vendor = :vendor),
                               :price,
                               :date
                        """, product_list)

        self.cursor.executemany("""
                INSERT OR IGNORE INTO prices (ProductID, VendorID, Price, Date)
                SELECT
                       (SELECT ID FROM products WHERE Product = :product),
                       (SELECT ID FROM vendors WHERE Vendor = :vendor),
                       :price,
                       :date
                WHERE EXISTS
                    (SELECT v.Vendor, p.ID, p.Product, pr.Price, pr.Date
                    FROM prices pr
                    INNER JOIN vendors v ON pr.VendorID = v.ID
                    INNER JOIN products p ON pr.ProductID = p.ID
                    WHERE p.Product = :product
                      AND v.Vendor = :vendor
                      AND pr.Price != :price
                      AND pr.Date != :date)
                """, product_list)

        # self.cursor.executemany("""
        # INSERT OR IGNORE INTO prices (ProductID, VendorID, Price, Date)
        # VALUES
        # ((SELECT ID from products WHERE Product=:product),
        # (SELECT ID from vendors WHERE Vendor=:vendor),
        # :price,
        # :date)
        # """, products)
