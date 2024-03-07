import time
import re
import random
import cloudscraper
import brotli
import json
import requests

class Pichau():
    
    def __init__(self, connector):
        store = None
        try:
            print('Buscando base URL')
            store = connector.get_store_track_url(2)
            self.track_url = store['base_url']
        except:
            print('Erro ao buscar base URL')
            self.track_url = "https://www.pichau.com.br/api/pichau/"
            pass
        

    
    def extrair_itens(self, product):
        # Procura pelo termo "Placa de Video" no início da string, ignorando maiúsculas/minúsculas e acentuação no "i"
        # print(product)
        string = product['name']
        match = re.match(r'Placa de V[íi]deo', string, re.IGNORECASE)
        
        
        if match:
            # Extrai o termo "Placa de Video"
            placa_de_video = match.group(0)
            
            # Restante da string após "Placa de Video"
            restante = string[match.end():].lstrip()
            # print(restante)
            # Se o restante começa com uma vírgula, remove-a e divide o restante por vírgulas
            itens_adicionais = restante.split(',')
            # Resultado final
            # print(itens_adicionais)
            final = [placa_de_video]
            x = 0        
            board = itens_adicionais[0].split(' ')
            # print(board)
            manufacturer = board[0]
            model_name =  ' '.join(board[1:])
            final = final + [manufacturer] + [model_name] + itens_adicionais[1:]
            for element in final:
                if element.startswith(" "):
                    final[x] = element.replace(' ', '')
                x += 1
            # print(final)
            final_dict = {
                'type': final[0],
                'manufacturer': final[1],
                'model': final[2],
                'memory': final[3],
                'memory_type': final[4],
                'memory_bus': final[5],
                'sku': final[6],
                'discount_price': product['discount_price'],
                'credit_price': product['credit_price'],
                'link': product['link'],
                'image': product['image'],
                'store_id': 2
            }
            return final_dict
        else:
            # Se "Placa de Video" não for encontrado, retorna a string inteira como um único elemento de lista
            final_str = string.split(',')
            board = final_str[0].split(' ')
            manufacturer = board[0]
            model_name = ' '.join(board[1:])
            final = [manufacturer] + [model_name] + final_str[1:]
            x = 0
            for element in final:
                if element.startswith(" "):
                    final[x] = element.replace(' ', '')
                x += 1
            # print(final)
            return {
                'type': "",
                'manufacturer': final[0],
                'model': final[1],
                'memory': final[2],
                'memory_type': final[3],
                'memory_bus': final[4],
                'sku': final[5],
                'discount_price': product['discount_price'],
                'credit_price': product['credit_price'],
                'link': product['link'],
                'image':  product['image'],
                'store_id': 2
            }


    def get_products(self, page=1):
        body = {
            "query" : "query GetCategoryAndAggregationsProducts($search: String, $filter: ProductAttributeFilterInput, $pageSize: Int!, $currentPage: Int!, $sort: ProductAttributeSortInput) {\n  products(\n    search: $search\n    filter: $filter\n    pageSize: $pageSize\n    currentPage: $currentPage\n    sort: $sort\n  ) {\n    total_count\n    page_info {\n      current_page\n      page_size\n      total_pages\n      __typename\n    }\n    items {\n      ...ProductItem\n      __typename\n    }\n    aggregations {\n      ...Aggregation\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ProductItem on ProductInterface {\n  id\n  name\n  sku\n  stock_status\n  __typename\n  url_key\n  informacoes_adicionais\n  product_page_layout\n  garantia\n  only_x_left_in_stock\n  amasty_label {\n    id\n    name\n    product_labels {\n      image\n      label\n      position\n      size\n      __typename\n    }\n    __typename\n  }\n  description {\n    html\n    __typename\n  }\n  small_image {\n    url\n    path\n    __typename\n  }\n  image {\n    url\n    path\n    __typename\n  }\n  media_gallery {\n    disabled\n    label\n    position\n    url\n    __typename\n  }\n  mysales_promotion {\n    expire_at\n    qty_available\n    qty_sold\n    price_discount\n    __typename\n  }\n  special_price\n  price_range {\n    minimum_price {\n      discount {\n        amount_off\n        percent_off\n        __typename\n      }\n      final_price {\n        currency\n        value\n        __typename\n      }\n      regular_price {\n        currency\n        value\n        __typename\n      }\n      __typename\n    }\n    maximum_price {\n      discount {\n        amount_off\n        percent_off\n        __typename\n      }\n      final_price {\n        currency\n        value\n        __typename\n      }\n      regular_price {\n        currency\n        value\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment Aggregation on Aggregation {\n  count\n  label\n  attribute_code\n  options {\n    count\n    label\n    value\n    __typename\n  }\n  __typename\n}",
            "variables" : {
                "search" : "rtx 4080",
                "filter" : {
                "forca" : {
                    "in" : [
                    "366"
                    ]
                },
                "placadevideo" : {
                    "in" : [
                    "130"
                    ]
                },
                "hide_from_search" : {
                    "eq" : "0"
                },
                "category_id" : {
                    "eq" : "2"
                }
                },
                "pageSize" : 100,
                "currentPage" : 1,
                "sort" : {
                "price" : "DESC"
                }
            },
            "operationName" : "GetCategoryAndAggregationsProducts"
            }
        headers = {
            'Host': 'www.pichau.com.br',
            'vendor': 'Pichau',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/json',
            'User-Agent': 'PichauMobile/67 CFNetwork/1490.0.4 Darwin/23.2.0',
            'Accept-Language': 'pt-BR,pt;q=0.9',
            'Authorization': '',
            'Content-Length': '2310',
            'Accept-Encoding': 'gzip, deflate, br'
        }
        while True:  # Loop infinito para continuar tentando até encontrar produtos
            print('Buscando na API')
            scraper = cloudscraper.create_scraper(delay=10)
            url = "https://www.pichau.com.br/api/pichau/"
            # print("Getting page", url)
            # resposta = scraper.post(url, json=self.body, headers=self.headers)
            resposta = scraper.post(url, json=body, headers=headers)
            print(resposta)
            # print(resposta.headers)
            produtos = []
            elementos_produto = {}
            
            try:
                elementos_produto = json.loads(resposta.content)
            except json.decoder.JSONDecodeError:
                return {'produtos': produtos}

            base_url = self.track_url.split('/api')[0]

            # Parseando o HTML com BeautifulSoup
              # Ajuste a classe conforme necessário
            elementos_produto = elementos_produto['data']['products']['items']
            for produto in elementos_produto:
                try:
                    produtos.append({
                        'name': produto['name'],
                        'discount_price': round(produto['price_range']['minimum_price']['final_price']['value']*0.85, 2),
                        'credit_price': produto['price_range']['minimum_price']['final_price']['value'],
                        'link': base_url + '/' + produto['url_key'],
                        'image': produto['small_image']['url']
                    })
                except (AttributeError, TypeError) as e:
                    pass  # Ignorar erros e continuar o loop

            if len(produtos) > 0:
                return {'produtos': produtos}
            else:
                # Espera por um tempo aleatório entre 5 e 10 segundos antes de tentar novamente
                wait_time = random.randint(5, 10)
                # print(f"Nenhum produto encontrado, tentando novamente em {wait_time} segundos...")
                time.sleep(wait_time)
    

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