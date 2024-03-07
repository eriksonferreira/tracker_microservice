from cachetools import Cache

# Inicializando o cache
cache = Cache(maxsize=1024)  # Define o tamanho máximo do cache

def add_or_update_cache(key, new_value):
    actual_value = cache.get(key)
    
    if actual_value is None:
        # print(f"Adicionando {key}: {new_value} ao cache.")
        cache[key] = new_value
        return True, None
    elif actual_value != new_value:
        # print(f"Atualizando {key} no cache de {actual_value} para {new_value}.")
        cache[key] = new_value
        return False, actual_value
    else:
        # print(f"Valor para {key} não mudou; mantendo {actual_value} no cache.")
        return  None, None
    

    
