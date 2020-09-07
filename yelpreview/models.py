from django.db import models
from register.models import User, Partner, ApiMap
from main.models import Service

from django.db.models.signals import post_save
from django.dispatch import receiver
from .yelp_review_getter import fetch_yelp_review
import logging
# Create your models here.

class yelpReview(models.Model):
    yelpBusinessId = models.ForeignKey(
            ApiMap,
            blank=False,
            null=False,
            on_delete=models.CASCADE
    )
    rating = models.DecimalField(max_digits=10, decimal_places=1, blank=False, null=False)
    comment = models.TextField(blank=False, null=False)
    tag = models.TextField(default='')

    def __str__(self):
        return '{} - {}'.format(self.yelpBusinessId, self.id)

@receiver(post_save, sender=ApiMap, dispatch_uid="fetch_review")
def fetch_review(sender, instance, created, **kwargs):
    if created:
        logger = logging.getLogger(__name__)
        review_data = fetch_yelp_review(instance)
        if not review_data:
            logger.error('Error while fetchhing reviews for ' + instance.businessPartner.businessName)
        else:
            for comment, rating, tag in review_data:
                yelpReview.objects.create(yelpBusinessId = instance, rating = rating, comment = comment, tag = tag)
        print('success')
