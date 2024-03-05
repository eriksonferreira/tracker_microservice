def new_best_price_str(product, old):
    text_message = f"""
    Novo melhor preço encontrado!
    {product['type']} {product['manufacturer']} {product['model']} {product['memory']}
    Preço antigo: R${old['prices'][0]['actual_price']}
    Preço atual: R${product['discount_price']}
    Preço no crédito: 12x{round((product['credit_price']/12), 2)}
    Link: {product['link']}
"""
    return text_message
    
def new_best_credit_price_str(product, old):
    text_message = f"""
    Novo melhor preço no crédito encontrado!
    {product['type']} {product['manufacturer']} {product['model']} {product['memory']}
    Preço antigo: R${old['prices'][0]['actual_price']}
    Preço atual: R${product['discount_price']}
    Preço no crédito: 12x{round((product['credit_price']/12), 2)}
    Link: {product['link']}
"""
    return text_message
    
def price_increased(product, old):
    text_message = f"""
    Preço aumentou :(
    {product['type']} {product['manufacturer']} {product['model']} {product['memory']}
    Preço antigo: R${old['prices'][0]['actual_price']}
    Preço atual: R${product['discount_price']}
    Preço no crédito: 12x{round((product['credit_price']/12), 2)}
    Link: {product['link']}
"""
    return text_message

def credit_price_increased(product, old):
    text_message = f"""
    Preço aumentou :(
    {product['type']} {product['manufacturer']} {product['model']} {product['memory']}
    Preço antigo: R${old['prices'][0]['actual_price']}
    Preço atual: R${product['discount_price']}
    Preço no crédito: 12x{round((product['credit_price']/12), 2)}
    Link: {product['link']}
"""
    return text_message