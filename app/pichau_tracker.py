import requests
from bs4 import BeautifulSoup
import requests
import time
import re
import random
import cloudscraper
class Pichau():
    
    def __init__(self, connector):
        store = connector.get_store_track_url(2)
        self.track_url = store['base_url']

    
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
                'previous_price': product['previous_price'],
                'discount_price': product['discount_price'],
                'credit_price': product['credit_price'],
                'credit_info': product['credit_info'],
                'link': product['link'],
                'image': "not_implemented"
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
                'previous_price': product['previous_price'],
                'discount_price': product['discount_price'],
                'credit_price': product['credit_price'],
                'credit_info': product['credit_info'],
                'link': product['link'],
                'image': "not_implemented"
            }


    def get_products(self, page=1):
        while True:  # Loop infinito para continuar tentando até encontrar produtos
            scraper = cloudscraper.create_scraper(
                browser={
                    'browser': 'firefox',
                    'platform': 'windows',
                    'mobile': False
                }, delay=10)
            page_str = f"&p={page}"
            url =  self.track_url + page_str
            # print("Getting page", url)
            resposta = scraper.get(url).content
            base_url = self.track_url.split('/s')[0]
            html = resposta

            # Parseando o HTML com BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            produtos = []
            elementos_produto = soup.find_all('div', class_='MuiGrid-item')  # Ajuste a classe conforme necessário

            for produto in elementos_produto:
                try:
                    name = produto.find('h2').get_text(strip=True)
                    previous_price = produto.find('s').get_text(strip=True)[3:].replace(',', '')
                    discount_price = produto.find('div', class_='jss83').get_text(strip=True)[3:].replace(',', '')
                    credit_info_div = produto.find('div', class_='jss109')
                    credit_price = credit_info_div.find('div', class_='jss110').get_text(strip=True)[3:].replace(',', '')
                    credit_info = credit_info_div.find('span', class_='jss112 jss113').get_text(strip=True)
                    link = base_url + produto.find('a', class_='jss12')['href']

                    produtos.append({
                        'name': name,
                        'previous_price': float(previous_price),
                        'discount_price': float(discount_price),
                        'credit_price': float(credit_price),
                        'credit_info': credit_info,
                        'link': link,
                        'image': "not_implemented"
                    })
                except (AttributeError, TypeError) as e:
                    pass  # Ignorar erros e continuar o loop

            if len(produtos) > 0:
                return {'produtos': produtos}
            else:
                # Espera por um tempo aleatório entre 5 e 10 segundos antes de tentar novamente
                wait_time = random.randint(5, 10)
                print(f"Nenhum produto encontrado, tentando novamente em {wait_time} segundos...")
                time.sleep(wait_time)
    

    def get_all_pages(self):
        print("Getting all products")
        prod = {'produtos': []}
        for page in range(1, 2, 1):
            # print(f"page {page}")
            informacoes_produtos = self.get_products(page)
            print(informacoes_produtos)
            # print(informacoes_produtos)
            try:
                prod['produtos'].extend(informacoes_produtos['produtos'])
            except ValueError:
                pass
            wait_time = range(0, 10, 1)
            choosed_time = random.choice(wait_time)
            print(F"Waiting for {choosed_time} seconds")
            time.sleep(choosed_time)
        print("Done!")
        print(f"Found {len(prod['produtos'])} products.")
        
        return prod
    

    def get_scrape_produts(self):
        products_cleansed = {'produtos': []}
        products = self.get_all_pages()
        # print(products)
        print("Processing strings..")
        for product in products['produtos']:
            try:
                prod = self.extrair_itens(product)
                products_cleansed['produtos'].extend([prod])
            except IndexError:
                continue

        print("Done!")

        return products_cleansed