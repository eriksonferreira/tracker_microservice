from connector import Connect
from operations import get_scrape_data, add_products
import os
import time
import random
import requests
from cache import add_or_update_cache
from get_products_externally import get_json_from_external_website
import json

os.environ['PYTHONWARNINGS'] = "ignore:Unverified HTTPS request"
os.environ['API_HOST'] = "https://price-tracker-ugjo2rw7cq-uc.a.run.app/"

api = Connect(os.environ['API_HOST'])
print("Initiating tracker..")

def initialize_cache():
    products = requests.get(os.environ['API_HOST']+"/products?limit=999&offset=0")
    products = products.json()
    products = products['data']
    # print(f"Gravando {len(products)} produtos no cache")
    # print(products)
   
    for product in products:
        try:
            add_or_update_cache(product['sku'], product['prices'][0]['actual_price'])
        except IndexError:
            pass

def get_update_time():
    time = requests.get(os.environ['API_HOST']+"/stores/2")
    time = time.json()
    # print(time)
    min_time = time['update_min_time']
    max_time = time['update_max_time']
    try:
        if min_time is not None and max_time is not None:
            return min_time, max_time
        else:
            return 360, 600
    except IndexError:
        return 360, 600
    

def get_pichau():

    filtered = []
    print("----------------------------------------------")
    print("Getting products for Pichau..")
    try:
        products = get_scrape_data(api, 2)
        for product in products['produtos']:

            cached, old_price = add_or_update_cache(product['sku'], product['discount_price'])
            # print(f"Cached: {cached} --- Old price: {old_price}")

            if cached:
                filtered.append(product)
            #     print("NAO ERA CACHEADO")

            if old_price is not None and product['discount_price'] < old_price:
                filtered.append(product)
            
            if old_price is not None and product['discount_price'] > old_price:
                filtered.append(product)

        if len(filtered) > 0:
            # print(f"Adding {len(filtered)} products to database..")
            if api is not None:
                for attempt in range(3):
                    try:
                        add_products(api, filtered)
                        print("Done!")
                        break
                    except requests.exceptions.ChunkedEncodingError:
                        time.sleep(2)
        else:
            print("Prices not changed")

    except:
        print("ERRO AO BUSCAR PICHAU, BUSCANDO EXTERNAMENTE")
        products = get_json_from_external_website('Pichau', api)
        del filtered

        filtered = []
        
        for product in products['produtos']:
            
            cached, old_price = add_or_update_cache(product['sku'], product['discount_price'])
            # print(f"Cached: {cached} --- Old price: {old_price}")

            if cached:
                filtered.append(product)
            #     print("NAO ERA CACHEADO")

            if old_price is not None and product['discount_price'] < old_price:
                filtered.append(product)
        
        if len(filtered) > 0:
            print(f"Adding {len(filtered)} products to database..")
            if api is not None:
                for attempt in range(3):
                    try:
                        add_products(api, filtered)
                        print("Done!")
                        break
                    except requests.exceptions.ChunkedEncodingError:
                        time.sleep(2)
        else:
            print("Prices not changed")        
    print("----------------------------------------------")


def get_terabyte():

    filtered = []
    print("Getting products for Terabyte..")
    try:
        products = get_scrape_data(api, 3)

        del filtered

        filtered = []
        
        for product in products['produtos']:
            
            cached, old_price = add_or_update_cache(product['sku'], product['discount_price'])
            # print(f"Cached: {cached} --- Old price: {old_price}")

            if cached:
                filtered.append(product)
            #     print("NAO ERA CACHEADO")

            if old_price is not None and product['discount_price'] < old_price:
                filtered.append(product)

            if old_price is not None and product['discount_price'] > old_price:
                filtered.append(product)

        
        if len(filtered) > 0:
            print(f"Adding {len(filtered)} products to database..")
            if api is not None:
                for attempt in range(3):
                    try:
                        add_products(api, filtered)
                        print("Done!")
                        break
                    except requests.exceptions.ChunkedEncodingError:
                        time.sleep(2)
        else:
            print("Prices not changed")

    except:
        print("ERRO AO BUSCAR TERABYTE, BUSCANDO EXTERNAMENTE")
        products = get_json_from_external_website('Terabyte', api)
        # print(products)
        del filtered

        filtered = []
        
        for product in products['produtos']:
            
            cached, old_price = add_or_update_cache(product['sku'], product['discount_price'])
            # print(f"Cached: {cached} --- Old price: {old_price}")

            if cached:
                filtered.append(product)
            #     print("NAO ERA CACHEADO")

            if old_price is not None and product['discount_price'] < old_price:
                filtered.append(product)
        
        if len(filtered) > 0:
            print(f"Adding {len(filtered)} products to database..")
            if api is not None:
                for attempt in range(3):
                    try:
                        add_products(api, filtered)
                        print("Done!")
                        break
                    except requests.exceptions.ChunkedEncodingError:
                        time.sleep(2)
        else:
            print("Prices not changed")
    print("----------------------------------------------")


def get_kabum():

    filtered = []
    print("Getting products for Kabum..")

    try:
        products = get_scrape_data(api, 4)

        del filtered

        filtered = []
        
        for product in products['produtos']:
            
            cached, old_price = add_or_update_cache(product['sku'], product['discount_price'])
            # print(f"Cached: {cached} --- Old price: {old_price}")

            if cached:
                filtered.append(product)
            #     print("NAO ERA CACHEADO")

            if old_price is not None and product['discount_price'] < old_price:
                filtered.append(product)
            
            if old_price is not None and product['discount_price'] > old_price:
                filtered.append(product)

        
        if len(filtered) > 0:
            print(f"Adding {len(filtered)} products to database..")
            if api is not None:
                for attempt in range(3):
                    try:
                        add_products(api, filtered)
                        print("Done!")
                        break
                    except requests.exceptions.ChunkedEncodingError:
                        time.sleep(2)
        else:
            print("Prices not changed")
        print("----------------------------------------------")

    except json.decoder.JSONDecodeError:
        print("ERRO AO BUSCAR TERABYTE, BUSCANDO EXTERNAMENTE")
        products = get_json_from_external_website('Kabum', api)
        del filtered

        filtered = []
        
        for product in products['produtos']:
            
            cached, old_price = add_or_update_cache(product['sku'], product['discount_price'])
            # print(f"Cached: {cached} --- Old price: {old_price}")

            if cached:
                filtered.append(product)
            #     print("NAO ERA CACHEADO")

            if old_price is not None and product['discount_price'] < old_price:
                filtered.append(product)
        
        if len(filtered) > 0:
            print(f"Adding {len(filtered)} products to database..")
            if api is not None:
                for attempt in range(3):
                    try:
                        add_products(api, filtered)
                        print("Done!")
                        break
                    except requests.exceptions.ChunkedEncodingError:
                        time.sleep(2)
        else:
            print("Prices not changed")


def orquestrate():
    try: 
        get_pichau()
    except:
        print("Error getting pichau")

    try: 
        get_terabyte()
    except:
        print("Error getting terabyte")

    try: 
        get_kabum()
    except:
        print("Error getting kabum")


    
    


    

    
    
initialize_cache()

while True:
    min_time, max_time = get_update_time()
    intervalo = random.randint(min_time, max_time)  # Gera um número aleatório entre x e y segundos obtidos via API
    orquestrate()
    print(f"Waiting for {intervalo} seconds..")
    time.sleep(intervalo)  # Pausa a execução pelo número de segundos gerado
      # Chama a função