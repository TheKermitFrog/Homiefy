from csv import DictReader
import string
import random
import os
import sys
import re
import datetime
from django.core.management import BaseCommand
from main.models import Service, Appointment
from register.models import Partner, User, ApiMap

class Command(BaseCommand):
    stealth_options = ("interactive",)
    # Show this when the user types help
    help = "Load yelp data"

    def handle(self, *args, **options):
        def get_random_string(length):
            letters = string.ascii_lowercase
            result_str = ''.join(random.choice(letters) for i in range(length))
            return result_str

        for row in DictReader(open('./service_complete_3.csv', encoding='utf-8-sig'), delimiter = ','):
            # Create user
            username = row['businessName'].replace(" ", "").lower()
            password = get_random_string(8)
            user = User.objects.create_user(username=username, password=password)
            user.first_name = "Manager of"
            user.last_name = row['businessName']
            user.phoneNumber = row['businessNumber']
            user.address = row['address']
            user.isPartner = True
            if row['email'] == "N/A":
                email = username + '@gmail.com'
            else:
                email = row['email']
            user.email = email
            user.save()
            print('Created user: ' + username + ' ' + 'password: ' + password, file=self.stdout)

            # Create partner
            partner = Partner.objects.create(user=user)
            partner.businessName = row['businessName']
            partner.businessNumber = row['businessNumber']
            partner.businessType = row['businessType']
            partner.description = row['description']
            partner.save()
            print('Created partner', file=self.stdout)

            # Create service accordingly
            for type in row['businessType'].split('/'):
                service = Service()
                service.businessPartner = partner
                service.type = type
                cap = [1, 2, 3]
                service.maxCapacity = random.choice(cap)
                price = [10.00, 15.00, 20.00, 25.00, 30.00, 35.00, 40.00, 45.00, 50.00]
                service.price = random.choice(price)
                duration = [30, 60, 90, 120, 180]
                service.duration = random.choice(duration)
                service.save()
                print('Created service ' + type, file=self.stdout)

            # Create ApiMap
            apimap = ApiMap.objects.create(businessPartner=partner, yelpBusinessId = row['yelpBusinessId'], yelpRating = row['yelpRating'], yelpCommentNum = row['yelpCommentNum'])
            print('Created apimap')
            print('-----------------------------------------')

        return
