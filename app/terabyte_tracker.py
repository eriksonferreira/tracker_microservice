import time
import re
import random
import cloudscraper
from bs4 import BeautifulSoup
import requests
import json

class Terabyte():
    
    def __init__(self, connector):
        store = None
        try:
            # print('Buscando base URL')
            store = connector.get_store_track_url(3)
            self.track_url = store['base_url']
            # print("Base URL: ", self.track_url)
        except:
            print('Erro ao buscar base URL')
            self.track_url = "https://www.terabyteshop.com.br/hardware/placas-de-video/nvidia-geforce"
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

            sku = ""
            if final[-1] == 'RayTracing':
                sku = '-'.join(final)
                sku = sku.replace(' ', '-')
            else:
                sku = final[-1]
            # print(final)
            final_dict = {
                'type': final[0],
                'manufacturer': final[1],
                'model': final[2],
                'memory': final[3],
                'memory_type': final[4],
                'memory_bus': final[5],
                'sku': sku,
                'discount_price': product['discount_price'],
                'credit_price': product['credit_price'],
                'link': product['link'],
                'image': product['image'],
                'store_id': 3
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
            if final[-1] == 'RayTracing':
                sku = '-'.join(final)
                sku = sku.replace(' ', '-')
            else:
                sku = final[-1]

            return {
                'type': "",
                'manufacturer': final[0],
                'model': final[1],
                'memory': final[2],
                'memory_type': final[3],
                'memory_bus': final[4],
                'sku': sku,
                'discount_price': product['discount_price'],
                'credit_price': product['credit_price'],
                'link': product['link'],
                'image':  product['image'],
                'store_id': 3
            }


    def get_products(self, page=1):
        # print('Buscando na API')
        scraper = cloudscraper.create_scraper(delay=20)
        url = self.track_url

        def get_body(page=''):
            body = f"app=true{page}&url=%2Fhardware%2Fplacas-de-video%2Fnvidia-geforce&filter%5Bmarca%5D=0&filter%5Border%5D=preco_asc&filter%5Bpg%5D=1&filter%5Bstr%5D=undefined"
            return body

        headers = {
            'Host': 'www.terabyteshop.com.br',
            'Connection': 'keep-alive',
            'Content-Length': '150',
            'Sec-Ch-Ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Sec-Ch-Ua-Mobile': '0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
            'Sec-Ch-Ua-Platform':	"Windows",
            'Origin': 'https://www.terabyteshop.com.br',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.terabyteshop.com.br/hardware/placas-de-video/nvidia-geforce',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            # 'Cookie': '__bid=8056e3d1-459b-4545-9eec-f51bd3653a8a; _gcl_au=1.1.1236685883.1708881818; _ga=GA1.1.1039661387.1708882033; _tt_enable_cookie=1; _ttp=_ltRLmgfDh5zV2UQ14rSIZPFLLa; smeventsclear_4949f4605c8043988cd9ac68408bb813=true; _hjSessionUser_597733=eyJpZCI6IjRhMzg2NWNhLTk3MzktNWRhMy05NGYwLTZmMTEyNWNlMmMwYiIsImNyZWF0ZWQiOjE3MDg4ODIwNDY1NzMsImV4aXN0aW5nIjp0cnVlfQ==; __udf_j=d11d15716e974693c6435f82f8c3d0e98887725b6856ffc47a158bba815caa7cead4dc1c0292f3cebb115586485710e9; RKT=false; _gcl_aw=GCL.1709087359.CjwKCAiArfauBhApEiwAeoB7qEYtFAhQhWfs2g0ZTLYG_MDW_9gwMKTVc0o3o2xGRIoAUAS76vwigBoCi-gQAvD_BwE; sm_event_impact=[{"gclid":"Cj0KCQiA5-uuBhDzARIsAAa21T8k6vYNmD6W-qITHABWv23AtOBClQIOI32GgmwiR5K7n15uPrkNxfYaAvMAEALw_wcB","create_date":"2024-02-25 15:45:31","path":"/"},{"utm_source":"banner_site","utm_medium":"banner_desktop","utm_campaign":"memorias_xpg_20_02_2023_q1","create_date":"2024-02-25 15:46:44","path":"/busca"},{"gclid":"CjwKCAiAivGuBhBEEiwAWiFmYQHH5AF_OzS2Xc4R2uTKQ1blexelIbeyZL8L-pl91utU5FIdxySvVRoCZ_cQAvD_BwE","create_date":"2024-02-26 21:35:47","path":"/"},{"gclid":"CjwKCAiAivGuBhBEEiwAWiFmYQHH5AF_OzS2Xc4R2uTKQ1blexelIbeyZL8L-pl91utU5FIdxySvVRoCZ_cQAvD_BwE","create_date":"2024-02-26 21:36:55","path":"/"},{"gclid":"CjwKCAiArfauBhApEiwAeoB7qEYtFAhQhWfs2g0ZTLYG_MDW_9gwMKTVc0o3o2xGRIoAUAS76vwigBoCi-gQAvD_BwE","create_date":"2024-02-27 23:29:23","path":"/"}]; PHPSESSID=rp4ij92456qtjekg3hk02b1fn7; cf_clearance=VqvHBWJguJk_CjtaaL0PvCoSouPaz387mbNEOxfkaFY-1709576558-1.0.1.1-9mkr_VHrghuUIQhv41Rb2qG03k3xdBmCvuqA980pEw96mbJoEXOFG4WVmjL1jPlZ0FbogZeVOosPetRRCeqp5A; key=5f0fd4e33c51035b355d5afb7dfb6797; __cf_bm=K8OzJRMPlLRGht_CgPVfjbqrynr89QfQHyaFzt55ZgE-1709592344-1.0.1.1-VMA0H14dOJ0BECOBd8afEAWtHXxpc8XTW5A.dww2ABugaKcMfOsIUTr7D_mWauQCJrN6wuP8id5FUlbb5tWhqhi8826qKyFA_aaZeDrpwk0; _hjSession_597733=eyJpZCI6IjM2NDg3ODZiLTI1NGYtNDZjMC1hMmRhLWYzZWY1YTg2ODkzNSIsImMiOjE3MDk1OTIzNDYzMzksInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; tbspops=1; smeventssent_4949f4605c8043988cd9ac68408bb813=true; _ga_R1DM0Q8KM0=GS1.1.1709592346.14.1.1709592455.58.0.0; cto_bundle=RUGBHF84dVF3UDUlMkZQeXB4eThCdnJGMk5KaGxQaFdjdjRsenVrd3JXTGYweUxRaDQ5VjFiMGVnMWJ2TSUyRlpwdW4yZHpBb2hWUnIzeWJMYUo0UkY0dFNSQSUyQlQ2d28lMkZ4UzlzZzhqbmlaakF1a21sZGNoWXlRQTlKU0xpV1hIN1JWTEpsTU50WG1KaUQzcUsyZnZDY0F6UFNnR3BVRDRUUm5RQVlOdSUyRnpRQWJ3M0FuWEhnJTNE',
            # 'X-Postman-Captr': '3105371',
            # '__cf_bm': 'Ow1IRLpZ9pwvpBRrLI.FZwbfW8zoOF7DwsT8qCDkIsI-1709856949-1.0.1.1-vWptkJRLbDwALeCpQ9HAV8jOmdM0MhYUxNaonz76FhX6Z4N4d.u7EsrafQq1AyyXXLVYiKGT60PU41Z31tbIYkWcxJszpI39hanOD1iFgYQ'
        }


        while True:  # Loop infinito para continuar tentando até encontrar produtos
            
            # print("Getting page", url)
            # resposta = scraper.post(url, json=self.body, headers=self.headers)
            
            # proxies = {"http": "http://localhost:5559", "https": "http://localhost:5559"}
            bodys = ['', '&more=true']
            products = []
            for body in bodys:
                resposta = requests.post(url, data=get_body(body), headers=headers)

                # print(resposta.content)
                # resposta = requests.post(url, json=body, headers=headers, allow_redirects=False)
                t = resposta.text
                text_without_bom = t.encode().decode('utf-8-sig')
                json_prod = json.loads(text_without_bom)
                html = ''
                if body == '':
                    html = json_prod['body']
                else:
                    html = json_prod['more']
                # print(resposta.headers)
                # print(resposta.content)
                # html = t['more']
                # print(html)
                soup = BeautifulSoup(html, 'html.parser')

                # Find all elements that might contain the GPU names and prices
                # This might require adjusting based on the actual structure of the HTML content
                gpu_elements = soup.find_all("div", class_="pbox col-xs-12 col-sm-6 col-md-3 col-lg-1-5")
                # print(gpu_elements)
                # Parseando o HTML com BeautifulSoup
                # Ajuste a classe conforme necessário
                
                for gpu in gpu_elements:
                    try:
                        # Extract the GPU name
                        all_sold = gpu.button
                        # print("all sold", all_sold)

                        if all_sold is None:
                            pass
                            # print("todos vendidos")
                        else:
                            name_element = gpu.find("h2")
                            name = name_element.text if name_element else "Name not found"

                            calc_price_credit = lambda preco_com_desconto: preco_com_desconto / 0.85

                            
                            # Extract the price
                            price_element = gpu.find("div", class_="prod-new-price")
                            # print(price_element)
                            price = price_element.text.strip() if price_element else "Price not found"
                            # print(price)
                            price = round(float(price.split(" ")[1].replace('.', '').replace(',', '.')), 2)
                            price_credit =  round(calc_price_credit(price), 2)
                            link = gpu.a['href']
                            imagem = gpu.find('div', class_='commerce_columns_item_image text-center').img['src']

                            product = {
                                'name': name,
                                'discount_price': price,
                                'credit_price': price_credit,
                                'link': link,
                                'image': imagem
                            }
                            products.append(product)
                            # print(product)
                            # break
                    except (AttributeError, TypeError) as e:
                        pass  # Ignorar erros e continuar o loop
                

            if len(products) > 0:
                print(f"Found {len(products)} products")
                return {'produtos': products}
            else:
                # Espera por um tempo aleatório entre 5 e 10 segundos antes de tentar novamente
                wait_time = random.randint(5, 10)
                # print(f"Nenhum produto encontrado, tentando novamente em {wait_time} segundos...")
                time.sleep(wait_time)


    def get_scrape_produts(self):
        products_cleansed = {'produtos': []}
        products = self.get_products()
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