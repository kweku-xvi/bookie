import os
from dotenv import load_dotenv
from trycourier import Courier


client = Courier(auth_token=os.getenv('COURIER_TOKEN'))


def send_mail_verification(email:str, username:str, link:str):
    client.send_message(
        message={
            "to": {
            "email": email,
            },
            "template": "HQRFKDHDK84B16GJAQ7PWPFATXS8",
            "data": {
            "username":username,
            "link": link,
            },
        }
    )