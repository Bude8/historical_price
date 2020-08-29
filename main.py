from vendors import *
from users import User
from database import Database
import requests

url_list = [line.rstrip() for line in open("links.txt")]

sainsburys_list = [Sainsburys(product_url) for product_url in url_list if "sainsburys" in product_url]
asos_list = [Asos(product_url) for product_url in url_list if "asos" in product_url]

vendor_list = [sainsburys_list, asos_list]

with Database('prices.db') as db:
    for vendor in vendor_list:
        db.insert_product_into_products_table_if_new(vendor)
        db.insert_price_into_prices_table_if_changed(vendor)


print("Today's prices:")
print("----------------- Sainsbury's -----------------")
print_prices(sainsburys_list)

print("----------------- ASOS -----------------")
print_prices(asos_list)

