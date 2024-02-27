from connector import Connect
from messages import new_best_price_str
from pichau_tracker import Pichau
from operations import get_scrape_data, add_pichau_products
import os
import time
import random

api = Connect('http://' + os.environ['API_HOST'])
print("Initiating tracker..")

def orquestrate():
    products = get_scrape_data(api)
    print("Adding products to database..")
    add_pichau_products(api, products['produtos'])
    print("Done!")

while True:
    intervalo = random.randint(30, 120)  # Gera um número aleatório entre 30 e 120 segundos
    print(f"Waiting for {intervalo} seconds..")
    time.sleep(intervalo)  # Pausa a execução pelo número de segundos gerado
    orquestrate()  # Chama a função