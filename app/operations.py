from pichau_tracker import Pichau
import time

def get_scrape_data(api):
    pichau = Pichau(api)
    products = pichau.get_scrape_produts()
    return products

def add_pichau_products(api, products):
    for product in products:
        r = api.add_product(product)
        r_json = r.json()
        # print(r_json)
        if r.status_code == 409:
            # print("Product exists!")
            product_info = {
                'product_id': r_json['detail']['product_details']['id'],
                'store_id': 2,
                'price': product['discount_price'],
                'price_credit': product['credit_price'],
                'url': product['link'],
                'date': int(time.time())
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
                'product_id': r_json['detail']['product_details']['id'],
                'store_id': 2,
                'actual_price': product['discount_price'],
                'actual_price_credit': product['credit_price'],
                'all_time_low': product['discount_price']
            }
            p = api.add_prices(product_info_prices)
            p_json = p.json()
            if p.status_code == 200:
                pass
                # print("Price added successfuly")
            else:
                pass
                # print("Error adding Price", p_json)
        elif r.status_code == 200:
            # print("Product added successfuly")
            
            product_info = {
                'product_id': r_json['id'],
                'store_id': 2,
                'price': product['discount_price'],
                'price_credit': product['credit_price'],
                'url': product['link'],
                'date': int(time.time())
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
                'store_id': 2,
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