# https://irkutsk.hh.ru/applicant/vacancy_response?vacancyId=90015384&hhtmFrom=vacancy
import requests
import json
import re


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

ses = requests.Session()


def get_book_author(data):
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

        self.r = ses.get(url, params=params, headers=request_headers)

        return self.r.json()


    def add_to_cart(self):
        # 3 books
        search_result = self.search("тестирование")["included"][:3] 
        request_headers["Cookie"] = '__ddg1_=iSoz5RdJHhSIumMpnaVl; access-token=Bearer%20eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDEzMjIyMjMsImlhdCI6MTcwMTE1NDIyMywiaXNzIjoiL2FwaS92MS9hdXRoL2Fub255bW91cyIsInN1YiI6ImJmYWZjOWQwOGM3YWViOWUzZjM2ZmE2MjU0NTdkYWE0ZTEyYmMzZTE2MWI4NzI0ZTYwYTc2NzVlZTQwMzBlMjQiLCJ0eXBlIjoxMH0.Qe837oM1P6txaOQ1GyykICNg530wc7tdZoZFkgsF8KI; chg_visitor_id=1ed8aac4-6498-4703-8465-df3b788075c9; refresh-token=;'
        
        url = BASE_URL + '/api/v1/cart/product'

        for book in search_result:
            r = ses.post(
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
        r = ses.get(url, headers=request_headers)
        books_in_cart = create_a_dict_from_json(r)

        return books_in_cart


    def compare_books_data_and_books_data_in_cart(self):
        '''
        Проверить , что в корзине находятся все выбранные книги, 
        в нужном количество, 
        за выбранную цену.

        Проверить что итоговая цена заказа равна сумме стоимостей всех выбранных книг.
        '''
        search_result = self.search("тестирование")["included"][:3]
        books_in_cart = self.show_cart()

        # treat search_result & books_in_cart as str
        # for re
        # compare by book_id, price
        search_result_book_ids = re.findall(r"'code': '(.*?)',", str(search_result)) # -> []
        search_result_book_prices = re.findall(r"'price': (.*?),", str(search_result)) # -> []
        
        books_in_cart_book_ids = re.findall(r"'book_id': (.*?),", str(books_in_cart)) # -> []
        books_in_cart_book_prices = re.findall(r"'price': (.*?),", str(books_in_cart)) # -> []

        
        print(
            sorted(search_result_book_ids), 
            sorted(books_in_cart_book_ids),
            sorted(search_result_book_prices),
            sorted(books_in_cart_book_prices),
            sorted(search_result_book_ids) == sorted(books_in_cart_book_ids),
            sorted(search_result_book_prices) == sorted(books_in_cart_book_prices)
        )
        

        '''
        for i in range(3):
            title = search_result[i]["attributes"]["title"]
            book_author = get_book_author(search_result[i]["attributes"])          
            book_id = search_result[i]["attributes"]["code"]
            price = search_result[i]["attributes"]["price"]
            url = search_result[i]["attributes"]["category"]["url"]

            book_ids.append(book_id)
            prices.append(price)

            print(f"Book_id:{book_id} in books_in_cart:{str(books_in_cart)}, price in prices")
        '''



    def delete(self):
        url = BASE_URL + '/api/v1/cart'

        r = ses.delete(url, headers=request_headers)
        print(r.status_code)




c = ChitayGorod()
#c.delete()
# print(c.show_cart())
#c.add_to_cart()
c.compare_books_data_and_books_data_in_cart()

s = '''
{0: {'title': 'Тестирование JavaScript', 'author': 'Лукас да Коста', 'book_id': 2954717, 'quantity': 1, 'cost': 2599, 'discount': 86, 'price': 2513, 'url': 'product/testirovanie-javascript-2954717'}, 1: {'title': 'Тестирование бизнес-идей', 'author': 'Александр Остервальдер', 'book_id': 2803288, 'quantity': 1, 'cost': 2099, 'discount': 311, 'price': 1788, 'url': 'product/testirovanie-biznes-idey-2803288'}, 2: {'title': 'Тестирование на проникновение с Kali Linux', 'author': 'Пранав Джоши', 'book_id': 2948959, 'quantity': 1, 'cost': 1099, 'discount': 316, 'price': 783, 'url': 'product/testirovanie-na-proniknovenie-s-kali-linux-2948959'}}
[Finished in 1.5s]
'''

books_in_cart_book_ids = re.findall(r"'book_id': (.*?),", str(s)) # -> []
#print(books_in_cart_book_ids)
