import requests
from kabum_tracker import Kabum
from pichau_tracker import Pichau
from terabyte_tracker import Terabyte

def get_json_from_external_website(store, api):

    r = requests.get(f'https://www.placasdevideo.app.br/precos/{store}.json')
    r = r.json()
    # print(r)
    tracker = None

    if store == 'Terabyte':
        tracker = Terabyte(api)

    elif store == 'Pichau':
        tracker = Pichau(api)
        
    elif store == 'Kabum':
        tracker = Kabum(api)

    products = []
    for gpu in r:
        name = gpu['Modelo']
        price = gpu['ValorAV']
        price_credit = gpu['ValorAV']*0.85 if store == 'Terabyte' else gpu['ValorParc']
        link = gpu['Link']
        imagem = ""

        product = {
            'name': name,
            'discount_price': price,
            'credit_price': price_credit,
            'link': link,
            'image': imagem
        }

        products.append(product)

    products = {'produtos': products}
    products_cleansed = {'produtos': []}
    # print(products)
    # print("Processing strings..")
    for product in products['produtos']:
        try:
            prod = tracker.extrair_itens(product)
            # print(prod)
            products_cleansed['produtos'].extend([prod])
        except IndexError as e:
            # print(e)
            continue

    # print(products_cleansed)

    return products_cleansed