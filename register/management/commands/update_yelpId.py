from register.models import Partner, User, ApiMap
from yelpreview.models import yelpReview
from django.core.management import BaseCommand
from register.find_yelp_id import *
import time
import logging

class Command(BaseCommand):
    stealth_options = ("interactive",)
    # Show this when the user types help
    help = "Monthly check for update"

    def handle(self, *args, **options):
        logger = logging.getLogger(__name__)
        # search yelp_id for business not having one

        # buisness list having an id
        names = ApiMap.objects.values_list('businessPartner__businessName', flat=True).distinct()

        partners = Partner.objects.exclude(businessName__in = names)

        for partner in partners:
            num = phone_transformer(partner.businessNumber)
            response = search_biz_by_num(num)

            if response:
                biz_data = get_biz_id(response, partner.businessType.split('/')[0], partner.businessName)
                if biz_data:
                    apimap = ApiMap.objects.create(businessPartner=partner, yelpBusinessId = biz_data['id'], yelpRating = biz_data['rating'], yelpCommentNum = biz_data['review_cnt'])
                else:
                    logger.error(partner.businessName + ' not in Yelp search result by phone number.')
            else:
                logger.error('Could not search ' + partner.businessName + 'by phone number.')

            time.sleep(5)
