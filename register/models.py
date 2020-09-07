from django.db import models
from django.contrib.auth.models import AbstractUser
from .find_yelp_id import *
from django.contrib.auth.models import User
import logging

# Create your models here.
class User(AbstractUser):
    address = models.TextField()
    phoneNumber = models.CharField(max_length=15)
    isPartner = models.BooleanField('partner status', default=False)
    isUser = models.BooleanField('user status', default=False)

class Partner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    businessType = models.CharField(max_length=50)
    businessName = models.CharField(max_length=50)
    businessNumber = models.CharField(max_length=15)
    description = models.TextField()


    def save(self, *args, **kwargs):
        super(Partner, self).save(*args, **kwargs)
        logger = logging.getLogger(__name__)
        if not ApiMap.objects.filter(businessPartner__businessName = self.businessName):
            num = phone_transformer(self.businessNumber)
            response = search_biz_by_num(num)

            if response:
                biz_data = get_biz_id(response, self.businessType.split('/')[0], self.businessName)
                if biz_data:
                    apimap = ApiMap.objects.create(businessPartner=Partner.objects.get(pk=self.pk), yelpBusinessId = biz_data['id'], yelpRating = biz_data['rating'], yelpCommentNum = biz_data['review_cnt'])
                else:
                    logger.error(self.businessName + ' not in Yelp search result by phone number.')
            else:
                logger.error('Could not search ' + self.businessName + 'by phone number.')




    def __str__(self):
        return '{} by {}'.format(self.businessType, self.businessName)

class ApiMap(models.Model):
    businessPartner = models.OneToOneField(Partner, on_delete=models.CASCADE, primary_key=True)
    yelpBusinessId = models.CharField(max_length=50, blank=False, null=False)
    yelpRating = models.DecimalField(max_digits=10, decimal_places=1, blank=False, null=False)
    yelpCommentNum = models.IntegerField(blank=False, null = False)

    def __str__(self):
        return '{} - {}'.format(self.businessPartner.businessName, self.yelpBusinessId[:5])
