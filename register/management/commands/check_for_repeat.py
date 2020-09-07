from yelpapi import YelpAPI
import requests
import re
from difflib import SequenceMatcher
from register.models import Partner, User, ApiMap
from django.core.management import BaseCommand

class Command(BaseCommand):
    stealth_options = ("interactive",)
    # Show this when the user types help
    help = "Loads data"

    def handle(self, *args, **options):
        maps = ApiMap.objects.all()

        name_map = {}
        for map in maps:
            name = map.businessPartner.businessName
            if name in name_map:
                name_map[name] += 1
            else:
                name_map[name] = 1

        for key in name_map:
            if name_map[key] > 1:
                print(str(key) + str(name_map[key]), file=self.stdout)
