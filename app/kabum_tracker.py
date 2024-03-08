import time
import re
import random
import cloudscraper
import brotli
import json
import requests

class Kabum():
    
    def __init__(self, connector):
        store = None
        try:
            print('Buscando base URL')
            store = connector.get_store_track_url(4)
            self.track_url = store['base_url']
        except:
            print('Erro ao buscar base URL')
            self.track_url = "https://servicespub.prod.api.aws.grupokabum.com.br/catalog/v2/products-by-category/hardware/placa-de-video-vga/placa-de-video-nvidia?facet_filters=ewoKfQ%3D%3D&page_number=1&page_size=100&sort=-price"
            pass
        

    
    def extrair_itens(self, product_name):
        sep = product_name['name'].split(',')
        # print(sep)
        try:
            memory = sep[1].split(' ')[1]
            memory_type = sep[1].split(' ')[-1]
            # print(memory, memory_type)
        except:
            print('ERROR IN ', sep)
            memory = ''
            memory_type = ''
            pass

        model_sep = sep[0].split('RTX')
        type_prod = model_sep[0]
        model = 'RTX' + model_sep[-1]
        sku_sep = sep[-1].split(' - ')
        sku = ''
        if len(sku_sep[-1]) > 5:
            sku = sku_sep[-1]
        else:
            sku = sep[-1]

        
        final_dict = {
                    'type': type_prod,
                    'manufacturer': product_name['manufacturer'],
                    'model': model,
                    'memory': memory,
                    'memory_type': memory_type,
                    'sku': sku,
                    'discount_price': product_name['discount_price'],
                    'credit_price': product_name['credit_price'],
                    'link': product_name['link'],
                    'image': product_name['image'],
                    'store_id': 4
                }
        return final_dict


    def get_products(self, page=1):

        headers = {
            'Host': 'servicespub.prod.api.aws.grupokabum.com.br',
            'Accept': 'application/json',
            'Accept-Language': 'pt-BR,q=1.0',
            'Accept-Encoding': 'br;q=1.0, gzip;q=0.9, deflate;q=0.8',
            'Origin': 'app.kabum.com.br',
            'User-Agent': 'Kabum/3.1.4 (br.com.kabum; build:1.0.12461; iOS 17.3.1) Alamofire/5.6.2',
            'Referer': 'app.kabum.com.br',
            'FMAPP1029384756': 'app.kabum.com.br'
        }
        print('Buscando na API')
        url = self.track_url
        # print("Getting page", url)
        # resposta = scraper.post(url, json=self.body, headers=self.headers)
        scraper = cloudscraper.create_scraper(delay=10)
        resposta = scraper.get(url, headers=headers)
        t = resposta.json()
        quantidade = len(t['data'])
        base_url = "https://www.kabum.com.br/produto"
        prods = []
        # print(quantidade)
        for prod in t['data']:
            name = prod['attributes']['title']
            credit_price = prod['attributes']['price']
            actual_price = prod['attributes']['price_with_discount']
            url = base_url + '/' + prod['links']['self'].split('/')[-1]
            image = prod['attributes']['photos']['g'][0]
            manufacturer = prod['attributes']['manufacturer']['name']
            product = {
                'name': name,
                'discount_price': actual_price,
                'credit_price': credit_price,
                'link': url,
                'image': image,
                'manufacturer': manufacturer,
            }
            prods.append(product)

        
        return {'produtos': prods}
            
    

    def get_all_pages(self):
        # print("Getting all products")
        prod = {'produtos': []}
        for page in range(1, 2, 1):
            # print(f"page {page}")
            informacoes_produtos = self.get_products(page)
            # print(informacoes_produtos)
            # print(informacoes_produtos)
            try:
                prod['produtos'].extend(informacoes_produtos['produtos'])
            except ValueError:
                pass
            wait_time = range(0, 10, 1)
            choosed_time = random.choice(wait_time)
            # print(F"Waiting for {choosed_time} seconds")
            time.sleep(choosed_time)
        # print("Done!")
        print(f"Found {len(prod['produtos'])} products.")
        
        return prod
    

    def get_scrape_produts(self):
        products_cleansed = {'produtos': []}
        products = self.get_all_pages()
        # print(products)
        # print("Processing strings..")
        for product in products['produtos']:
            try:
                prod = self.extrair_itens(product)
                products_cleansed['produtos'].extend([prod])
            except IndexError:
                continue

        # print("Done!")

        return products_cleansed