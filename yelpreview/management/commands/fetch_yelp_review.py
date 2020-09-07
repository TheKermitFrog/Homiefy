import requests
import time
from nltk.tokenize import word_tokenize
from nltk import bigrams, trigrams
import re
from register.models import Partner, User, ApiMap
from yelpreview.models import yelpReview
from django.core.management import BaseCommand
import ast

class Command(BaseCommand):
    stealth_options = ("interactive",)
    # Show this when the user types help
    help = "Loads data"

    def handle(self, *args, **options):
        # map = ApiMap.objects.get(businessPartner__businessName='Weed Man')
        maps = ApiMap.objects.all()
        nlp_file = open('./nlp_dict.txt', 'r').read()
        nlp_dict = ast.literal_eval(nlp_file)
        for map in maps:
            print('Fetching reviews for ' + map.businessPartner.businessName)

            business_id = map.yelpBusinessId
            business_type = map.businessPartner.businessType


            total = 1
            offset = 0
            while offset < total:
                ajax_api = f'https://www.yelp.com/biz/{business_id}/review_feed?rl=en&sort_by=relevance_desc&q=&start={offset}'
                resp = requests.get(ajax_api)
                if resp.status_code != 200:
                    print(map.businessPartner.businessName + ' reviews are not fetched correctly')
                resp.raise_for_status()
                data = resp.json()
                pagination = data['pagination']
                total = pagination['totalResults']
                offset += pagination['resultsPerPage']

                reviews = data['reviews']

                tag = ''
                for review in reviews:
                    comment = review['comment']['text']

                    # single word match
                    tokenize_1 = word_tokenize(comment)
                    # remove punctuations
                    for word in tokenize_1:
                        if re.match(r'^\W+$', word):
                            tokenize_1.remove(word)

                    for type in business_type.split('/'):
                        list = nlp_dict.get(type)
                        if list:
                            for word in tokenize_1:
                                if word in list:
                                    tag += type + '/'

                # bi-grams match if non-matched from 1st match
                    if not tag:
                        bigram = [' '.join(w) for w in bigrams(tokenize_1)]
                        for type in business_type.split('/'):
                            list = nlp_dict.get(type)
                            if list:
                                for bi in bigram:
                                    if bi in list:
                                        tag += type + '/'

                # tri-grams match
                    if not tag:
                        trigram = [' '.join(w) for w in trigrams(tokenize_1)]
                        for type in business_type.split('/'):
                            list = nlp_dict.get(type)
                            if list:
                                for tri in trigram:
                                    if bi in list:
                                        tag += type + '/'

                    yelpReview.objects.create(yelpBusinessId = map, rating = review['rating'], comment = comment, tag = tag)
                print('Reviews fetched for ' + map.businessPartner.businessName)
                time.sleep(1)
