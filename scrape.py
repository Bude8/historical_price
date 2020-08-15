from bs4 import BeautifulSoup
from vendors import *
from datetime import date
import requests

sainsburys_domain = "https://www.sainsburys.co.uk"
sainsburys_subdomain = "/groceries-api/gol-services/product/v1/product"
query_params = "?filter[product_seo_url]=gb/groceries/"

innocent_plus_wonder_green = "https://www.sainsburys.co.uk/groceries-api/gol-services/product/v1/product?filter[product_seo_url]=gb%2Fgroceries%2Finnocent-wonder-green-750ml&include[ASSOCIATIONS]=true&include[DIETARY_PROFILE]=true"
guiness = "https://www.sainsburys.co.uk/groceries-api/gol-services/product/v1/product?filter[product_seo_url]=gb%2Fgroceries%2Fguinness-draught-stout-10x440ml&include[ASSOCIATIONS]=true&include[DIETARY_PROFILE]=true"


rude_health_almond_milk_path = "rude-health-uht-almond-milk-1l"
rude_health_almond_milk = Sainsburys(rude_health_almond_milk_path)

print_prices(rude_health_almond_milk.name, rude_health_almond_milk.price, date.today())

url = "https://www.asos.com/asos-design/asos-design-stretch-slim-floral-shirt-in-navy-and-white/prd/20345910"
response = requests.get(url)
print(response)
