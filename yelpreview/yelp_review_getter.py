import requests
import time
from nltk.tokenize import word_tokenize
from nltk import bigrams, trigrams
import re
from register.models import Partner, User, ApiMap
# from yelpreview.models import yelpReview
from django.core.management import BaseCommand
import ast


def fetch_yelp_review(map):
    print('Fetching reviews for ' + map.businessPartner.businessName)

    business_id = map.yelpBusinessId
    business_type = map.businessPartner.businessType



    nlp_file = open('./nlp_dict.txt', 'r').read()
    nlp_dict = ast.literal_eval(nlp_file)

    offset = 0
    total = 1
    output = []
    while offset < total:
        ajax_api = f'https://www.yelp.com/biz/{business_id}/review_feed?rl=en&sort_by=date_desc&q=&start={offset}'
        try:
            resp = requests.get(ajax_api)
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            return None
        data = resp.json()
        pagination = data['pagination']
        total = pagination['totalResults']
        offset += pagination['resultsPerPage']

        reviews = data['reviews']

        tag = ''

        for review in reviews:
            comment = review['comment']['text']
            rating = review['rating']

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

            output.append([comment, rating, tag])

    print('Reviews fetched for ' + map.businessPartner.businessName)
    return(output)

def fetch_new_yelp_review(map, diff):
    print('Fetching new reviews for ' + map.businessPartner.businessName)

    business_id = map.yelpBusinessId
    business_type = map.businessPartner.businessType

    nlp_file = open('./nlp_dict.txt', 'r').read()
    nlp_dict = ast.literal_eval(nlp_file)

    offset = 0
    output = []
    ind = 0
    while offset < diff:
        ajax_api = f'https://www.yelp.com/biz/{business_id}/review_feed?rl=en&sort_by=date_desc&q=&start={offset}'
        try:
            resp = requests.get(ajax_api)
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            return None
        data = resp.json()
        pagination = data['pagination']
        total = pagination['totalResults']
        offset += pagination['resultsPerPage']

        reviews = data['reviews']

        tag = ''
        while ind < diff:
            review = reviews[ind]
            comment = review['comment']['text']
            rating = review['rating']

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

            output.append([comment, rating, tag])
            ind += 1

    print('New reviews fetched for ' + map.businessPartner.businessName)
    return(output)
