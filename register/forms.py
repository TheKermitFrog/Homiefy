from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django import forms

from register.models import User, Partner

class UserSignUpForm(UserCreationForm):
    phone_number = forms.CharField(max_length=12, required=True)
    address = forms.CharField(max_length=200, required=True)

    class Meta(UserCreationForm.Meta):
        fields = ('username','first_name','last_name','email','password1','password2')
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.isUser = True
        user.phoneNumber = self.cleaned_data.get('phone_number')
        user.address = self.cleaned_data.get('address')
        user.save()
        return user

class PartnerSignUpForm(UserCreationForm):
    phone_number = forms.CharField(max_length=12, required=True)
    address = forms.CharField(max_length=200, required=True)
    businessName = forms.CharField(max_length=50, required=True)
    businessNumber = forms.CharField(max_length=12, required=True)
    businessType = forms.CharField(max_length=20, required=True)
    description = forms.CharField(max_length=200, required=True)

    class Meta(UserCreationForm.Meta):
        fields = ('username','email','password1','password2','first_name','last_name')
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.isPartner = True
        user.phoneNumber = self.cleaned_data.get('phone_number')
        user.address = self.cleaned_data.get('address')
        user.save()
        partner = Partner.objects.create(user=user)
        partner.businessName = self.cleaned_data.get('businessName')
        partner.businessNumber = self.cleaned_data.get('businessNumber')
        partner.businessType = self.cleaned_data.get('businessType')
        partner.description = self.cleaned_data.get('description')
        partner.save()
        return user
