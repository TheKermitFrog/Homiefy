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
        API_KEY = '9soW6VogCkHI2uLtw5lsCXTxmI8IzRvSjyTrsglsf-BrTZoBQpNYjYjTKR3liWzxlecDvD3benPDgl_uptQ1jSGPbyFSxdg3h90-2hLkdtAsB8TepiKts4skBk8XX3Yx'
        API_HOST = 'https://api.yelp.com'
        BUSINESS_PATH = '/v3/businesses/search/phone?phone='

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

            response = requests.get(url, headers=headers)

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
                        if (category['title'] == biz_category) & (similar(biz['name'], biz_name) > 0.5):
                            return  { 'id' : biz['id'],
                                      'rating': biz['rating'],
                                      'review_cnt': biz['review_count']}
            return None


        partners = Partner.objects.all()

        for partner in partners:
            number = phone_transformer(partner.businessNumber)
            biz_category = partner.businessType.split('/')[0]
            biz_name = partner.businessName
            result = search_biz_by_num(number)
            yelp_data = get_biz_id(result, biz_category, biz_name)

            if yelp_data:
                print('business: ' + biz_name + 'id: ' + yelp_data['id'] + ' rating: ' + str(yelp_data['rating']) + ' cnt: ' + str(yelp_data['review_cnt']), file=self.stdout)
                apimap = ApiMap.objects.create(businessPartner=partner, yelpBusinessId = yelp_data['id'], yelpRating = yelp_data['rating'], yelpCommentNum = yelp_data['review_cnt'])
                apimap.save()
            else:
                print('business: ' + biz_name + ' data not found')

            # prevent too frquent call on the api
            time.sleep(0.5)
