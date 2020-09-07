from register.models import Partner, User, ApiMap
from yelpreview.models import yelpReview
from django.core.management import BaseCommand


class Command(BaseCommand):
    stealth_options = ("interactive",)
    # Show this when the user types help
    help = "Loads data"

    def handle(self, *args, **options):
        apis = ApiMap.objects.all()
        for api in apis:
            num = len(yelpReview.objects.filter(yelpBusinessId = api))
            if num != api.yelpCommentNum:
                print(api.businessPartner.businessName + 'cnt: ' + str(api.yelpCommentNum) + 'act: ' + str(num))
