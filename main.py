from database import Database
from vendors import *

url_list = [line.rstrip() for line in open("links.txt")]

sainsburys_products = [Sainsburys(product_url) for product_url in url_list if "sainsburys" in product_url]
asos_products = [Asos(product_url) for product_url in url_list if "asos" in product_url]
products_with_missing_prices = [product for product in asos_products if product.price is None]
asos_products = [product for product in asos_products if product.price is not None]

products_with_price_change = []
vendor_products_list = [sainsburys_products, asos_products]

with Database('prices.db') as db:
    for products in vendor_products_list:
        db.insert_product_into_products_table_if_new(products)
        db.insert_price_into_prices_table_if_changed(products)

print("Today's prices:")
print("----------------- Sainsbury's -----------------")
print_prices(sainsburys_products)

print("----------------- ASOS -----------------")
print_prices(asos_products)

print("----------------- Missing Prices -----------------")
print_prices(products_with_missing_prices)
