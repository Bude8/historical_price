import sqlite3

connection = sqlite3.connect('prices.db')

c = connection.cursor()
c.execute("pragma foreign_keys=ON;")

c.execute("DROP TABLE IF EXISTS vendors;")
c.execute("DROP TABLE IF EXISTS products;")
c.execute("DROP TABLE IF EXISTS prices;")
c.execute("DROP TABLE IF EXISTS users;")
c.execute("DROP TABLE IF EXISTS tracking;")

c.execute(
    """
    CREATE TABLE vendors (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Vendor TEXT UNIQUE
                )
    """
)

c.execute(
    """
    CREATE TABLE products (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Product TEXT,
                ProductURL TEXT,
                UNIQUE (ProductURL)
                )
    """
)

c.execute(
    """
    CREATE TABLE prices (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                ProductID INTEGER,
                VendorID INTEGER,
                Price REAL,
                Date INTEGER,
                FOREIGN KEY (ProductID) REFERENCES products (ID),
                FOREIGN KEY (VendorID) REFERENCES vendors (ID),
                UNIQUE (ProductID, VendorID, Date)
                )
    """
)

c.execute(
    """
    CREATE TABLE users (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                Email TEXT NOT NULL UNIQUE
                )
    """
)

c.execute(
    """
    CREATE TABLE tracking (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserID INTEGER,
                ProductID INTEGER,
                VendorID INTEGER,
                FOREIGN KEY (ProductID) REFERENCES products (ID),
                FOREIGN KEY (VendorID) REFERENCES vendors (ID),
                FOREIGN KEY (UserID) REFERENCES users (ID)
                )
    """
)

connection.close()
