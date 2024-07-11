import os, string, random, requests
from dotenv import load_dotenv


load_dotenv()


PAYSTACK_SECRET = os.getenv('PAYSTACK_SECRET')


def generate_id(num:int):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(num))


def initialize_transaction(amount:str, email:str, reference:str):
    url="https://api.paystack.co/transaction/initialize"

    headers = {
        'Authorization':f'Bearer {PAYSTACK_SECRET}'
    }

    data = {
        'email':email,
        'amount': amount,
        'reference':reference
    }

    response = requests.post(url=url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['data']['authorization_url']
    else:
        return response.json()['message']


def verify_payment(reference:str):
    url = "https://api.paystack.co/transaction/verify/{reference}"

    headers = {
        'Authorization':f'Bearer {PAYSTACK_SECRET}'
    }

    response = requests.get(url=url, headers=headers)

    if response.status_code == 200:
        return response.json()['data']