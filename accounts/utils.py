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


def contact_us_mail(subject:str, message:str, name:str, senders_email:str):
    client.send_message(
        message={
            "to": {
            "email": "nksarps@gmail.com",
            },
            "template": "7HHFJF15B4MZYBPX77K5C4WMBKJV",
            "data": {
            "subject": subject,
            "message": message,
            "name": name,
            "senders_email": senders_email,
            },
        }
    )


def contact_us_mail_response(email:str, name:str):
    client.send_message(
        message={
            "to": {
            "email": email,
            },
            "template": "9A0MXQA2CK4MR8KFNHPN67RH3SF9",
            "data": {
            "userName": name,
            },
        }
    )


def send_password_reset_mail(email:str, link:str, first_name:str):
    client.send_message(
        message={
            "to": {
            "email": email,
            },
            "template": "YGYJMP0VPTM47YHDY9QTRTH0MDJJ",
            "data": {
            "firstName": first_name,
            "link": link,
            },
        }
    )
