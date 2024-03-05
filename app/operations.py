from pichau_tracker import Pichau
from terabyte_tracker import Terabyte
import time
from history import check_history_price

def get_scrape_data(api, store_id):

    store = api.get_store_track_url(store_id)
    if store['name'] == "Pichau":
        pichau = Pichau(api)
        products = pichau.get_scrape_produts()
        return products
    elif store['name'] == "TerabyteShop":
        terabyte = Terabyte(api)
        products = terabyte.get_scrape_produts()
        return products

def add_products(api, products):
    for product in products:
        # print(product)
        r = api.add_product(product)

        r_json = r.json()
        # print(product)
        if r.status_code == 409:
            # print("Product exists!")
            product_info = {
                'product_id': r_json['detail']['product_details']['id'],
                'store_id': product['store_id'],
                'price': product['discount_price'],
                'price_credit': product['credit_price'],
                'url': product['link'],
                'date': int(time.time()),
                'other_info': product,
                'sku': product['sku'],
                'image': product['image']
            }
            new_best_price, prod_details = check_history_price(product_info, api)
            if new_best_price:
                h = api.add_history(product_info)
                h_json = h.json()
                price_id = prod_details['prices'][0]['id']
                if h.status_code == 200:
                    product_info_prices = {
                    'product_id': r_json['detail']['product_details']['id'],
                    'store_id': product['store_id'],
                    'actual_price': product['discount_price'],
                    'actual_price_credit': product['credit_price'],
                    'all_time_low': h_json['id'],
                    'price_id': price_id
                    }
                    p = api.update_prices(product_info_prices)
                    # print(p.content)
                    p_json = p.json()
                    if p.status_code == 200:
                        pass
                    else:
                        pass
                else:
                    
                    print("Error adding History", h_json)
                    product_info_prices = {
                    'product_id': r_json['detail']['product_details']['id'],
                    'store_id': product['store_id'],
                    'actual_price': product['discount_price'],
                    'actual_price_credit': product['credit_price'],
                    'price_id': price_id
                    }
                    p = api.update_prices(product_info_prices)
                    # print(p.content)
                    p_json = p.json()
                    if p.status_code == 200:
                        pass
                    else:
                        pass
                
                
                
            
        elif r.status_code == 200:
            # print("Product added successfuly")
            
            product_info = {
                'product_id': r_json['id'],
                'store_id': product['store_id'],
                'price': product['discount_price'],
                'price_credit': product['credit_price'],
                'url': product['link'],
                'date': int(time.time()),
                'sku': product['sku'],
                'image': product['image']
            }

            h = api.add_history(product_info)
            h_json = h.json()
            if h.status_code == 200:
                pass
                # print("Price added successfuly")
            else:
                pass
                # print("Error adding Price", p_json)
            product_info_prices = {
                'product_id': r_json['id'],
                'store_id': product['store_id'],
                'actual_price': product['discount_price'],
                'actual_price_credit': product['credit_price'],
                'all_time_low': h_json['id']
            }
            p = api.add_prices(product_info_prices)
            if p.status_code == 200:
                pass
                # print("Price added successfuly")
            else:
                pass
                # print("Error adding Price", p_json)