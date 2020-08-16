import sqlite3

connection = sqlite3.connect("prices.db")

# Vendors must match vendors.py class.vendor name AND be stored in the list as tuples
vendors_list = [
    ("asos", ),
    ("Sainsbury's", )
]

c = connection.cursor()

c.executemany("INSERT INTO vendors (Vendor) VALUES (?)", vendors_list)

connection.commit()

connection.close()
