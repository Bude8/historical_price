import requests



def print_prices(name, price, date):
    print("{} - £{:.2f} - {}".format(name, price, date))


class Sainsburys:
    def __init__(self, product_path):
        self.base_url = "https://www.sainsburys.co.uk/groceries-api/gol-services/product/v1/product"
        self.payload = {"filter[product_seo_url]": "gb/groceries/{}".format(product_path)}
        self.response = requests.get(self.base_url, params=self.payload)
        if self.response.status_code == 200:
            self.name = self.response.json()['products'][0]['name']
            self.price = float(self.response.json()['products'][0]['retail_price']['price'])


class Asos:
    def __init__(self, product_path):
        self.base_url = "https://www.asos.com/api/product/catalogue/v3/stockprice"
        self.payload = {"productIds": "{}".format(product_path), "store": "COM"}
        self.response = requests.get(self.base_url, params=self.payload)
        if self.response.status_code == 200:
            self.name = self.response.json()