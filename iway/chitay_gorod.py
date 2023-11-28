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


    def create_dict_of_first_three_books_of_search(self):
        search_result = self.search('тестирование')

        for i in range(3): 
            print(search_result["included"][i])


    def add_to_cart(self):
        books = self.get_first_three_books_of_search() 
        request_headers['Cookie'] = '__ddg1_=iSoz5RdJHhSIumMpnaVl; access-token=Bearer%20eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDEzMjIyMjMsImlhdCI6MTcwMTE1NDIyMywiaXNzIjoiL2FwaS92MS9hdXRoL2Fub255bW91cyIsInN1YiI6ImJmYWZjOWQwOGM3YWViOWUzZjM2ZmE2MjU0NTdkYWE0ZTEyYmMzZTE2MWI4NzI0ZTYwYTc2NzVlZTQwMzBlMjQiLCJ0eXBlIjoxMH0.Qe837oM1P6txaOQ1GyykICNg530wc7tdZoZFkgsF8KI; chg_visitor_id=1ed8aac4-6498-4703-8465-df3b788075c9; refresh-token=;'
        
        url = BASE_URL + '/api/v1/cart/product'
        for book_id in books:
            r = ses.post(
                url, 
                json={
                    "id":int(book_id),
                    "adData":{
                        "item_list_name":"search",
                        "product_shelf":""
                    }
                }, 
                headers=request_headers
            )    
        
    
    def create_dict_of_books_in_cart(self):
        url = BASE_URL + '/api/v1/cart'
        r = ses.get(url, headers=request_headers)
        cart_books = {}

        # create a dict
        for book_json in r.json()["products"]:
            author = get_book_author(book_json)
            discount = get_book_discount(book_json)
            cost = get_order_cost(r)

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
            
            print(book_info)
            
            # add this book info to dict
            # cart_books[r.json()["products"].index(book_json)] = book_info
           
        # return cart_books 
        

    def compare_books_data_and_books_data_in_cart(self):
        books_in_cart = self.create_dict_of_books_in_cart()
        first_three_books = self.create_dict_of_first_three_books_of_search()

        print(books_in_cart, "\n\n", first_three_books)






    
    def delete(self):

        url = BASE_URL + '/api/v1/cart'

        r = s.delete(url, headers=request_headers)
        print(r.headers)
        del s
 





c = ChitayGorod()
# c.delete()
# c.add_to_cart()
c.create_dict_of_books_in_cart()
