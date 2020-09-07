from yelpapi import YelpAPI
import requests
import re
from difflib import SequenceMatcher


API_KEY = '9soW6VogCkHI2uLtw5lsCXTxmI8IzRvSjyTrsglsf-BrTZoBQpNYjYjTKR3liWzxlecDvD3benPDgl_uptQ1jSGPbyFSxdg3h90-2hLkdtAsB8TepiKts4skBk8XX3Yx'
API_HOST = 'https://api.yelp.com'
BUSINESS_PATH = '/v3/businesses/search/phone?phone='
BUSINESS_ID_PATH = '/v3/businesses/'
# helper function for formatting phone number
def phone_transformer(number):
    return '+1'+''.join(re.findall(r'\d+', number))

# helper function for calculating similarity metric between two strings
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

#  search business within Yelp by matching phone number
def search_biz_by_num(businessNumber):
    business_path = BUSINESS_PATH + businessNumber
    url = API_HOST + business_path
    headers = {'Authorization': f"Bearer {API_KEY}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return None

    return response.json()

# get yelp_business_id from search result
def get_biz_id(response, biz_category, biz_name):
    if response['total'] == 0:
        return None
    if response['total'] == 1:
        return { 'id' : response['businesses'][0]['id'],
                  'rating' : response['businesses'][0]['rating'],
                   'review_cnt': response['businesses'][0]['review_count']}
    else:
        for biz in response['businesses']:
            for category in biz['categories']:
                if (category['title'] == biz_category) | (similar(biz['name'], biz_name) > 0.5):
                    return  { 'id' : biz['id'],
                                 'rating': biz['rating'],
                                    'review_cnt': biz['review_count']}
    return None

def search_data_by_id(businessId):
    business_path = BUSINESS_ID_PATH + businessId
    url = API_HOST + business_path
    headers = {'Authorization': f"Bearer {API_KEY}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return None

    return response.json()

def get_review_count(response):
    return response['review_count']

def get_rating(response):
    return response['rating']
