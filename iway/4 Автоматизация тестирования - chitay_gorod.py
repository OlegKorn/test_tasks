# https://irkutsk.hh.ru/applicant/vacancy_response?vacancyId=90015384&hhtmFrom=vacancy
import requests
import json
import re
import random


BASE_URL = 'https://web-gate.chitai-gorod.ru'

request_headers = {
    'Host': 'web-gate.chitai-gorod.ru',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Cache-Control': 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDEzMjIyMjMsImlhdCI6MTcwMTE1NDIyMywiaXNzIjoiL2FwaS92MS9hdXRoL2Fub255bW91cyIsInN1YiI6ImJmYWZjOWQwOGM3YWViOWUzZjM2ZmE2MjU0NTdkYWE0ZTEyYmMzZTE2MWI4NzI0ZTYwYTc2NzVlZTQwMzBlMjQiLCJ0eXBlIjoxMH0.Qe837oM1P6txaOQ1GyykICNg530wc7tdZoZFkgsF8KI',
    'Origin': 'https://www.chitai-gorod.ru',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://www.chitai-gorod.ru/',
    'Cookie': '__ddg1_=iSoz5RdJHhSIumMpnaVl; refresh-token=; access-token=Bearer%20eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDEzMjIyMjMsImlhdCI6MTcwMTE1NDIyMywiaXNzIjoiL2FwaS92MS9hdXRoL2Fub255bW91cyIsInN1YiI6ImJmYWZjOWQwOGM3YWViOWUzZjM2ZmE2MjU0NTdkYWE0ZTEyYmMzZTE2MWI4NzI0ZTYwYTc2NzVlZTQwMzBlMjQiLCJ0eXBlIjoxMH0.Qe837oM1P6txaOQ1GyykICNg530wc7tdZoZFkgsF8KI',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'TE': 'trailers'
}


def get_book_author(data):
    if data["authors"] == []:
        author = "No author"
        return author
    
    else:
        if data["authors"][0]["middleName"] != "":
            author = data["authors"][0]["firstName"] + " " + data["authors"][0]["middleName"] + " " +  data["authors"][0]["lastName"]
        else:
            author = data["authors"][0]["firstName"] + " " + data["authors"][0]["lastName"]

    return author
    

def get_book_discount(data):
    if data["fullCost"] and data["price"]:
        discount = int(data["fullCost"]) - int(data["price"])
    else: 
        discount = 0

    return discount


def get_order_cost(data):
    order_cost = data.json()["cost"]
    order_cost_with_sale = data.json()["costWithSale"]
    order_cost_with_bonuses = data.json()["costWithBonuses"]
    order_discount = data.json()["discount"]

    if order_cost_with_sale:
        order_cost = int(order_cost_with_sale)
    if not order_cost_with_sale:
        order_cost = int(r.json()["cost"])

    return order_cost


def create_a_dict_from_json(res, books={}):
    for book_json in res.json()["products"]:
        author = get_book_author(book_json)
        discount = get_book_discount(book_json)
        cost = get_order_cost(res)

        book_info = {
            "title": book_json["title"],
            "author": author,
            "book_id": book_json["goodsId"],
            "id": book_json["id"],
            "quantity": book_json["quantity"],
            "cost": int(book_json["fullCost"]),
            "discount": int(discount),
            "price": int(book_json["price"]),
            "url": book_json["url"]
        }
            
        # add this book info to dict
        books[res.json()["products"].index(book_json)] = book_info

    return books


class ChitayGorod:
    def search(self, phrase):
        url = BASE_URL + '/api/v2/search/product'

        params = {
            'phrase': f'{phrase}',
            'products[page]': '1',
            'products[per-page]': '48',
            'sortPreset': 'relevance'
        }

        self.r = requests.get(url, params=params, headers=request_headers)

        return self.r.json()


    def add_to_cart(self):
        # 1st 3 books
        search_result = self.search("тестирование")["included"][:3] 
        request_headers["Cookie"] = '__ddg1_=iSoz5RdJHhSIumMpnaVl; access-token=Bearer%20eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDEzMjIyMjMsImlhdCI6MTcwMTE1NDIyMywiaXNzIjoiL2FwaS92MS9hdXRoL2Fub255bW91cyIsInN1YiI6ImJmYWZjOWQwOGM3YWViOWUzZjM2ZmE2MjU0NTdkYWE0ZTEyYmMzZTE2MWI4NzI0ZTYwYTc2NzVlZTQwMzBlMjQiLCJ0eXBlIjoxMH0.Qe837oM1P6txaOQ1GyykICNg530wc7tdZoZFkgsF8KI; chg_visitor_id=1ed8aac4-6498-4703-8465-df3b788075c9; refresh-token=;'
        
        url = BASE_URL + '/api/v1/cart/product'

        for book in search_result:
            r = requests.post(
                url, 
                json={
                    "id":int(book["attributes"]["code"]),
                    "adData":{
                        "item_list_name":"search",
                        "product_shelf":""
                    }
                }, 
                headers=request_headers
            )             
            
            print(int(book["attributes"]["code"]), r.status_code)
        
        
    def show_cart(self) -> dict:
        url = BASE_URL + "/api/v1/cart"
        r = requests.get(url, headers=request_headers)
        books_in_cart = create_a_dict_from_json(r)

        return books_in_cart


    def get_order_price(self) -> int:
        url = BASE_URL + "/api/v1/cart"
        r = requests.get(url, headers=request_headers)
        
        order_total_cost = r.json()["costWithSale"]

        return order_total_cost


    def compare_books_data_and_books_data_in_cart(self):
        books_in_cart = self.show_cart()
        quantities = []

        # price * quantity
        for k, v in books_in_cart.items():
            price_and_quantity = str(v["price"]) + ":" + str(v["quantity"])
            quantities.append(price_and_quantity)

            v["price"] = int(v["price"]) * int(v["quantity"])

        books_in_cart_book_ids = re.findall(r"'book_id': (.*?),", str(books_in_cart)) # -> []
        books_in_cart_book_prices = re.findall(r"'price': (.*?),", str(books_in_cart)) # -> []

        total_order_price_calculated_from_cart = sum(map(int, books_in_cart_book_prices)) 
        total_order_price_gotten_from_cart = self.get_order_price()
        
        print(
            f"ids of cart books: {sorted(books_in_cart_book_ids)}\n",
            f"prices of cart books: {sorted(books_in_cart_book_prices)}\n", 
            f"quantities of cart books: {quantities}\n",
            f"prices calculated from cart: {total_order_price_calculated_from_cart}\n",
            f"order total price gotten from cart: {total_order_price_gotten_from_cart}\n",
            "Prices summated from cart are equal to prices gotten from cart: ", (total_order_price_calculated_from_cart == total_order_price_gotten_from_cart)
        )


    def delete_from_cart(self, delete_all=False):
        books_in_cart = self.show_cart()
        try:
            ids_for_deleting = re.findall(r"'id': (.*?),", str(books_in_cart)) # -> []
            print(ids_for_deleting)
            
            if delete_all:
                for i in ids_for_deleting:
                    url = BASE_URL + f"/api/v1/cart/product/{str(i)}"
                    r = requests.delete(url, headers=request_headers)
                    print(i, r.status_code)

            random_id = random.choice(ids_for_deleting)
   
            url = BASE_URL + f"/api/v1/cart/product/{str(random_id)}"
            r = requests.delete(url, headers=request_headers)
            print(random_id, r.status_code)
        
        except IndexError:
            print("Empty cart")
        



c = ChitayGorod()
#c.delete_from_cart()
#c.add_to_cart()
#print(c.show_cart())
#print(c.show_cart())
#print(c.get_order_price())


c.compare_books_data_and_books_data_in_cart()      # запускать отдельно от всех
