import requests
from tabulate import tabulate
from datetime import date


def print_prices(product_list):
    table = []
    for product in product_list:
        try:
            table.append([product.name, "£{:.2f}".format(product.price)])
        except TypeError:
            table.append([product.name, "N/A"])
    print(tabulate(table, headers=["Name", "Price"]), "\n")


def get_payload_product(product_url):
    split_string = product_url.split("/")
    return split_string[-1]


class Sainsburys:
    def __init__(self, product_url=None):
        self.product_url = product_url
        self.vendor = "Sainsbury's"

        if product_url is not None:
            self.base_url = "https://www.sainsburys.co.uk/groceries-api/gol-services/product/v1/product"
            self.payload = {"filter[product_seo_url]": "gb/groceries/{}".format(get_payload_product(product_url))}
            self.response = requests.get(self.base_url, params=self.payload)

        if self.response.status_code == 200:
            self.name = self._get_product_name(self.response)
            self.price = self._get_price(self.response)

    def _get_product_name(self, response):
        return response.json()['products'][0]['name']

    def _get_price(self, response):
            return float(response.json()['products'][0]['retail_price']['price'])


class Asos:
    def __init__(self, product_url=None):
        self.product_url = product_url
        self.vendor = "asos"

        if product_url is not None:
            self.base_url = "https://www.asos.com/api/product/catalogue/v3/stockprice"
            self.payload = {"productIds": "{}".format(get_payload_product(product_url)), "store": "COM"}
            self.response = requests.get(self.base_url, params=self.payload)

        if self.response.status_code == 200:
            self.name = self._get_product_name(product_url)
            self.price = self._get_price(self.response)

    def _get_product_name(self, product_url):
        split_string = product_url.replace("-", " ").split("/")
        return split_string[-3]

    def _get_price(self, response):
        try:
            return float(response.json()[0]['productPrice']['current']['value'])
        except IndexError:
            return None
