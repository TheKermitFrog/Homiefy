import string
import random
from django.core.management import BaseCommand
from register.models import User

class Command(BaseCommand):
    stealth_options = ("interactive",)
    # Show this when the user types help
    help = "Loads data from test_data.csv into songs model"

    def handle(self, *args, **options):

        # generate random password
        def get_random_string(length):
            letters = string.ascii_lowercase
            result_str = ''.join(random.choice(letters) for i in range(length))
            return result_str

        for i in range(0, 10):
            username = 'user' + get_random_string(8)
            password = get_random_string(8)
            user = User.objects.create_user(username=username, password=password)
            user.first_name = 'Auto'
            user.last_name = 'Generated' + i

        return
