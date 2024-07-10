import os, qrcode, requests
from trycourier import Courier
from dotenv import load_dotenv

load_dotenv()

client = Courier(auth_token=os.getenv('COURIER_TOKEN'))
client_id = os.getenv('IMGUR_CLIENT_ID')


def send_booking_confirmation_email(email:str, first_name:str, event_name:str, ticket_id:str, date:str, time:str, location:str, img_url:str):
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
                "image_url":img_url,
            },
        }
    )


def generate_qrcode(ticket_id: str):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(ticket_id)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    file_name = 'qrimage.png'
    img.save(file_name)
    return file_name


def upload_to_imgur(file_path):
    headers = {'Authorization': f'Client-ID {client_id}'}
    with open(file_path, 'rb') as img:
        response = requests.post(
            'https://api.imgur.com/3/upload',
            headers=headers,
            files={'image': img}
        )
    if response.status_code == 200:
        data = response.json()
        return data['data']['link']
    else:
        print(f"Failed to upload image: {response.status_code} {response.text}")
        return None



