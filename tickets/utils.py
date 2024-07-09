import os
from trycourier import Courier
from dotenv import load_dotenv

load_dotenv()

client = Courier(auth_token=os.getenv('COURIER_TOKEN'))

def send_booking_confirmation_email(email:str, first_name:str, event_name:str, ticket_id:str, date:str, time:str, location:str):
    client.send_message(
        message={
            "to": {
            "email": email,
            },
            "template": "ZZYXN40DE2MSEWHM8Z02NCJN5WAQ",
            "data": {
                "firstName": first_name,
                "eventName":event_name,
                "bookingReference": ticket_id,
                "eventDate": date,
                "eventTime": time,
                "eventLocation": location,
            },
        }
    )