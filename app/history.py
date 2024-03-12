from messages import new_best_price_str, new_best_credit_price_str, credit_price_increased, price_increased

def check_history_price(product_info, connector):
    r = connector.get_products_by_id(product_info['product_id'])
    try:
        if round(float(product_info['price']), 2) < round(float(r['prices'][0]['actual_price']), 2):
            print('new_best_price')
            connector.send_telegram_message({
                'image_url': product_info['other_info']['image'],
                'text': new_best_price_str(product_info['other_info'], r)
            })
            return True, r
        elif round(float(product_info['price']), 2) > round(float(r['prices'][0]['actual_price']), 2):
            print('price increased')
            connector.send_telegram_message({
                'image_url': product_info['other_info']['image'],
                'text': price_increased(product_info['other_info'], r)
            })
            return True, r

    except:
        pass
    try:
        if round(float(product_info['price_credit']), 2) < round(float(r['prices'][0]['actual_price_credit']), 2):
            print('new_best_credit_price')
            connector.send_telegram_message({
                'image_url': product_info['other_info']['image'],
                'text': new_best_credit_price_str(product_info['other_info'], r)
            })
            return True, r
        elif round(float(product_info['price_credit']), 2) > round(float(r['prices'][0]['actual_price_credit']), 2):
            print('credit_price increased')
            connector.send_telegram_message({
                'image_url': product_info['other_info']['image'],
                'text': credit_price_increased(product_info['other_info'], r)
            })
            return True, r
    except:
        pass
    
    return False, r