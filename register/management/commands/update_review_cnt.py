from register.models import Partner, User, ApiMap
from yelpreview.models import yelpReview
from django.core.management import BaseCommand
from register.find_yelp_id import *
from yelpreview.yelp_review_getter import fetch_new_yelp_review
import time
import logging

class Command(BaseCommand):
    stealth_options = ("interactive",)
    # Show this when the user types help
    help = "Monthly check for update"

    def handle(self, *args, **options):
        logger = logging.getLogger(__name__)

        # buisness list having an id
        maps = ApiMap.objects.all()

        for map in maps:
            response = search_data_by_id(map.yelpBusinessId)

            if response:
                review_cnt = get_review_count(response)
                if review_cnt != map.yelpCommentNum:
                    diff = review_cnt - map.yelpCommentNum
                    map.yelpCommentNum = review_cnt
                    map.yelpRating = get_rating(response)
                    map.save()
                    if diff > 0:
                        review_data = fetch_new_yelp_review(map, diff)
                        if not review_data:
                            logger.error('Error while fetchhing reviews for ' + map.businessPartner.businessName)
                        else:
                            for comment, rating, tag in review_data:
                                yelpReview.objects.create(yelpBusinessId = map, rating = rating, comment = comment, tag = tag)
                    else:
                        logger.error(map.businessPartner.businessName + 'has inconsistency between two APIs')

            else:
                logger.error('Response error for ' + map.businessPartner.businessName + 'by Yelp id.')

            time.sleep(5)
