from csv import DictReader
import datetime
import string
import random
import os
import sys
import re
import datetime
from django.core.management import BaseCommand
from main.models import Service, Appointment
from register.models import Partner, User



class Command(BaseCommand):
    stealth_options = ("interactive",)
    # Show this when the user types help
    help = "Loads data"



    def handle(self, *args, **options):

        # generate random password
        def get_random_string(length):
            letters = string.ascii_lowercase
            result_str = ''.join(random.choice(letters) for i in range(length))
            return result_str

        for row in DictReader(open('./cs411_data.csv', encoding='utf-8-sig'), delimiter = ','):
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

                ##### Leave this part for creating random appointment
                #### Problems: Prolly needs some user to work with
                # num = [0, 0, 0, 0, 0, 1 ,2 ,3]
                # appointment_num = random.choice(num)
                # datetime_increment = datetime.timedelta(hours = service.duration // 60, minutes = service.duration % 60)
                #
                # for i in range(0, appointment_num):
                #     bookings = Appointment.objects.filter(service=self.service).filter(startTime__gte=datetime.date.today() + datetime.timedelta(days=1))
                #
                #     available_date = [datetime.date.today() + datetime.timedelta(days=x) for x in range(1, 14)]
                #     booked_time = {}
                #
                #     # populate available choices of time
                #     for date in available_date:
                #         start_time = datetime.datetime.combine(date, datetime.time(9, 00))
                #         booked_time[start_time] = 0
                #         start_time = start_time + datetime_increment
                #         while start_time < datetime.datetime.combine(date, datetime.time(18, 00)):
                #             booked_time[start_time] = 0
                #             start_time = start_time + datetime_increment
                #
                #     for booking in bookings:
                #         time = booking.startTime.astimezone(pytz.timezone('America/Chicago')).replace(tzinfo=None)
                #         booked_time[time] += 1
                #         booked_time[time + datetime_increment] += 1
                #
                #
                #     timechoice = []
                #     for key in booked_time:
                #         if booked_time[key] < maxCapacity:
                #             timechoice.append((key, key.strftime("%m/%d/%Y, %H:%M")))
                print('-----------------------------------------')

        return
