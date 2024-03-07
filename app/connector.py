import requests
import time
class Connect():


    def __init__(self, api_host) -> None:
        # print(api_host)
        self.api_host = api_host
        self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        while True:
            r = requests.get(api_host)
            if r.status_code == 200:
                r = r.json()
                print(f"{r['message']} - API initialized.")
                break
            else:
                print("API Offline, reconeting in 30 seconds..")
                time.sleep(30)
            
    


    def post(self, json, endpoint):
        r = requests.post(self.api_host+endpoint, json=json, headers=self.headers, verify=False)
        return r.text()
        

    def add_new_product(self, product):
        r = requests.post(self.api_host, json=product, headers=self.headers, verify=False)


    def get_products(self):
        r = requests.get(self.api_host+"/products", headers=self.headers, verify=False)
        return r.json()
    
    
    def get_products_by_id(self, id):
        r = requests.get(self.api_host+f"/products/{id}", headers=self.headers, verify=False)
        return r.json()
    
    
    def get_store_track_url(self, id):
        r = requests.get(self.api_host+f"/stores/{id}", headers=self.headers, verify=False)
        return r.json()
    
    
    def add_product(self, product):
        r = requests.post(self.api_host+"/products", json=product, headers=self.headers, verify=False)
        return r
    
    
    def add_history(self, product_info):
        r = requests.post(self.api_host+"/historys", json=product_info, headers=self.headers, verify=False)
        return r
    

    def add_prices(self, product_info):
        r = requests.post(self.api_host+"/prices", json=product_info, headers=self.headers)
        return r
    
    def send_telegram_message(self, message):
        r = requests.post(self.api_host+"/telegram/send_message", json=message, headers=self.headers)
        return r
    
    def update_prices(self, product_info):
        # print(product_info)
        r = requests.put(self.api_host+f"/prices/{product_info['price_id']}", json=product_info, headers=self.headers)
        return r
    