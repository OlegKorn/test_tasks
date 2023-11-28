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

        return self.r


    def get_first_three_books_of_search(self):
        search_result = self.search('тестирование')
        
        # get the first three books price, title, urls
        # book_ids = [self.r.json()['data']['relationships']['products']['data'][i]['id'] for i in range(3)] 
        
        print(search_result.json()["included"][0])


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

        order_cost = r.json()["cost"]
        order_cost_with_sale = r.json()["costWithSale"]
        order_cost_with_bonuses = r.json()["costWithBonuses"]
        order_discount = r.json()["discount"]

        if order_cost_with_sale:
            order_cost = int(order_cost_with_sale)
        if not order_cost_with_sale:
            order_cost = int(r.json()["cost"])

        print(
            order_cost, 
            order_cost_with_sale,
            order_cost_with_bonuses
        )

        cart_books = {}

        # create a dict
        for book_json in r.json()["products"]:
            # element_index = r.json()["products"].index(book_json)
            if book_json["authors"][0]["middleName"] != "":
                author = book_json["authors"][0]["firstName"] + " " + book_json["authors"][0]["middleName"] + " " +  book_json["authors"][0]["lastName"]
            else:
                author = book_json["authors"][0]["firstName"] + " " + book_json["authors"][0]["lastName"]

            if book_json["fullCost"] and book_json["price"]:
                discount = int(book_json["fullCost"]) - int(book_json["price"])
            else: 
                discount = 0

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
            cart_books[r.json()["products"].index(book_json)] = book_info

        return cart_books 
        

    def compare_books_data_and_books_data_in_cart(self):
        books_in_cart = self.create_dict_of_books_in_cart()
        first_three_books = self.get_first_three_books_of_search()

        print(books_in_cart, "\n\n", first_three_books)



    def check_books_by_id(self):
        books_in_cart = self.create_dict_of_books_in_cart()
        first_three_books = self.get_first_three_books_of_search()

        print(books_in_cart, "\n\n", first_three_books)


    def delete(self):

        url = BASE_URL + '/api/v1/cart'

        r = s.delete(url, headers=request_headers)
        print(r.headers)
        del s
 





c = ChitayGorod()
# c.delete()
# c.add_to_cart()
c.get_first_three_books_of_search()