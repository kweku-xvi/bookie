import os
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from dotenv import load_dotenv


load_dotenv()

class Command(BaseCommand):
    help = 'Creates a superuser.'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(email=os.getenv('ADMIN_EMAIL')).exists():
            User.objects.create_superuser(
                email=os.getenv('ADMIN_EMAIL'),
                password=os.getenv('ADMIN_PASSWORD')
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully.'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists.'))