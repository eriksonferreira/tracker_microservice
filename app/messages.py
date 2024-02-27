def new_best_price_str(product):
    text_message = f"""
    Novo melhor preço encontrado!
    {product['type']} {product['manufacturer']} {product['model']} {product['memory']}
    Preço atual: R${product['price']}
    Melhor preço em {product['all_time_low_date']} dias!!
    Link: {product['link']}
"""
    return text_message
    
