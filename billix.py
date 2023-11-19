import requests
from billix_config import *


class Test:

    def send_a_request(self, req_body, req_url):
        auth_token=self.auth()
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
            "X-XSRF-Token": f"{auth_token}"
        }

        self.response = requests.post(
            req_url, 
            headers=headers,
            json=req_body
        )

        print(self.response.json())


    def auth(self):
        request_body = {
            "email": e,
            "password": p
        }
        
        auth_url = f"{BASE_URL}/auth_v4/public/token"

        self.response = requests.post(
            auth_url, 
            headers=headers,
            json=request_body
        )

        if self.response.status_code <= 201:
            return self.response.json()["token"]
        else:            
            print("Error: ", self.response.status_code, self.response.reason)

            
    def create_a_client(self):
        request_body = {
            "company_uuid": f"{company_uuid}",
            "phone": "+79501103887",
            "email": "test@yopmail.com",
            "type": "individual"
        }
        create_a_client_url = f"{BASE_URL}/client/client"

        self.send_a_request(request_body, create_a_client_url)


    def create_a_cart(self):
        request_body = {
            "client_uuid": f"{client_uuid}"
        }
        create_cart_url = f"{BASE_URL}/cart/cart"

        self.send_a_request(request_body, create_cart_url)


    def add_operation_buy(self, auto_prolong=True):
        '''
        tariff_uuid - uuid тарифа
        price_uuid - uuid цены
        auto_prolong - флаг автопродления, говорит о том, будет ли услуга автоматически продлеваться после покупки. Если выставляется данный флаг,
                       то карта которой заплатит клиент должна автоматически привязаться к подписке.
        params - параметры операции (пустой объект)

        В ответ получим объект с uuid созданной операции
        {
            “uuid”: “string”,
            “modify_index”: 0
        }
        '''
        request_body = {
            "tariff_uuid": f"{tariff_uuid}",
            "price_uuid": f"{price_uuid}",
            "auto_prolong": auto_prolong,
            "params": {}
        }
        create_cart_url = f"{BASE_URL}/cart/cart/{cart_uuid}/operation/buy"

        self.send_a_request(request_body, create_cart_url)

    
    def add_operation_prolong(self, need_change=False):
        '''
        Если не требуется изменение периода
        
        POST http://{{domain}}/cart/cart/{{cart_uuid}}/operation/prolong
        ‘{
            “service_uuid”: “string”
        }’
        
        service_uuid - uuid существующей подписки клиента, которую необходимо продлить
        В ответ получим объект с uuid созданной операции
        
        {
            “uuid”: “string”,
            “modify_index”: 0
        }
        
        С изменением периода или тарифа
        
        POST http://{{domain}}/cart/cart/{{cart_uuid}}/operation/prolong
        ‘{
        “service_uuid”: “string”,
        “new_price_uuid”: “string”,
        “new_tariff_uuid”: “string”
        }’
        new_price_uuid - uuid существующей цены по тарифу подписки, отличный от текущей
        new_tariff_uuid - uuid существующего тарифа, отличный от текущего
        В ответ получим объект с uuid созданной операции
        {
        “uuid”: “string”,
        “modify_index”: 0
        }
        '''
        if need_change:
            request_body = {
                # new_price_uuid - uuid существующей цены по тарифу подписки, отличный от текущей
                # new_tariff_uuid - uuid существующего тарифа, отличный от текущего
                "service_uuid": f"{operation_uuid}",
                "new_price_uuid": "",
                "new_tariff_uuid": ""
            }
        else:
            request_body = {
                # service_uuid - uuid существующей подписки клиента, которую необходимо продлить
                "service_uuid": f"{operation_uuid}"
            }
        
        prolong_url = f"{BASE_URL}/cart/cart/{cart_uuid}/operation/prolong"
        
        self.send_a_request(request_body, create_cart_url)


    def pay_for_cart(self):
        '''
        payment_method_uuid - uuid метода оплаты
        save_payment_method - флаг сохранения метода оплаты, учитывается если у метода оплаты есть возможность сохранить платежные данные, 
        сохраненные платежные данные в последствии будут использованы для автопродления. 
        Указываем true если у позиции корзины активно автопродление и false если оно не активно.
        В случае если в корзине бесплатная операция (триальная или с 0 ценой), то запрос выглядит так же, но в BODY не нужно ничего передавать.
        В ответ получим объект с uuid корзины
        bash
        {
        “uuid”: “string”,
        “modify_index”: 0
        }
        тестовая юкасса, оплата банковскими картами 420adaa3-183e-4a6f-9558-77702c7ae9b4
        Тестовая юкасса имеет возможность сохранения платежных данных.
        '''
        request_body = {
            "payment_method_uuid": "420adaa3-183e-4a6f-9558-77702c7ae9b4",
            "save_payment_method": True
        }

        pay_cart_url = f"{BASE_URL}/cartpay/cart/{cart_uuid}/pay"

        self.send_a_request(request_body, pay_cart_url)

    
    def get_payment_url(self):
        auth_token=self.auth()

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
            "X-XSRF-Token": f"{auth_token}"
        }

        self.response = requests.get(
            f"{BASE_URL}/cart/cart/{cart_uuid}", 
            headers=headers
        )
        
        payment_url = self.response.json()["payment_url"]
        print(payment_url)


t = Test()
# t.create_a_client()
# t.create_a_cart()

# case 1
'''
Проверка 
-Покупка подписки на месяц, 
-автопродление вкл, 
-успешная оплата
- "Платеж в статусе Зачислен"

Ожидаемое поведение
1 Карта сохраняется и привязывается к подписке
2 Подписка Активна
3 Автопродление включено
'''
# t.add_operation_buy(auto_prolong=True)
# t.pay_for_cart() 

# t.get_payment_url()





# ---------------------------------
# case 2
'''
actions:
-Покупка подписки на год,
- автопродление выключено, 
- успешная оплата   "Платеж в статусе Зачислен

must:
-Карта не сохраняется 
-Подписка Активна
-Автопродление отключено
'''

# t.add_operation_buy(auto_prolong=True)
# t.pay_for_cart() 

# t.get_payment_url()





# ---------------------------------
# case 3
'''
actions:
-Покупка подписки на год,
- автопродление выключено, 
- неуспешная оплата   "Платеж в статусе Зачислен

must:
-Платеж в статусе Отклонен
-Карта не сохраняется
-Подписка в статусе Заказана
-Доступна повторная оплата корзины
'''
#t.create_a_cart()
#t.add_operation_buy(auto_prolong=True)
#t.pay_for_cart()
t.get_payment_url()