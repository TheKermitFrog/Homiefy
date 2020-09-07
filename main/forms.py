from django import forms
from .models import Service, Appointment
from register.models import Partner
import datetime
import pytz

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('startTime',)

    def save(self):
        appointment = super().save(commit=False)
        appointment.service = self.service
        appointment.customer = self.user
        appointment.partner = self.service.businessPartner
        appointment.startTime = self.cleaned_data.get('startTime')
        appointment.endTime = appointment.startTime
        appointment.save()
        return appointment

    def __init__(self, *args, **kwargs):
        self.service = kwargs.pop('service',None)
        self.user = kwargs.pop('user',None)
        super(AppointmentForm, self).__init__(*args, **kwargs)
        maxCapacity = self.service.maxCapacity


        duration = self.service.duration
        datetime_increment = datetime.timedelta(hours = duration // 60, minutes = duration % 60)

        bookings = Appointment.objects.filter(service=self.service).filter(startTime__gte=datetime.date.today() + datetime.timedelta(days=1))

        available_date = [datetime.date.today() + datetime.timedelta(days=x) for x in range(1, 14)]
        booked_time = {}

        # populate available choices of time
        for date in available_date:
            start_time = datetime.datetime.combine(date, datetime.time(9, 00))
            booked_time[start_time] = 0
            start_time = start_time + datetime_increment
            while start_time < datetime.datetime.combine(date, datetime.time(18, 00)):
                booked_time[start_time] = 0
                start_time = start_time + datetime_increment

        for booking in bookings:
            time = booking.startTime.astimezone(pytz.timezone('America/Chicago')).replace(tzinfo=None)
            if(booking.customer == self.user):
                booked_time[time] = maxCapacity
            else:
                booked_time[time] += 1
                if booked_time.get(time + datetime_increment):
                    booked_time[time + datetime_increment] += 1


        timechoice = []
        for key in booked_time:
            if booked_time[key] < maxCapacity:
                timechoice.append((key, key.strftime("%m/%d/%Y, %H:%M")))


        self.fields['startTime'] = forms.ChoiceField(label="Select a start time:", choices=timechoice)



class ServiceForm(forms.ModelForm):
    # type = forms.CharField(max_length=50, required=True)
    # maxCapacity = forms.IntegerField(required=True)
    # price = forms.DecimalField(max_digits=36, decimal_places=2, required=True)

    class Meta:
        model = Service
        fields = ('type', 'maxCapacity', 'price', 'duration')

    # @transaction.atomic
    def save(self):
        service = super().save(commit=False)
        partner = Partner.objects.get(user=self.user)
        service.businessPartner = partner
        service.type = self.cleaned_data.get('type')
        service.maxCapacity = self.cleaned_data.get('maxCapacity')
        service.price = self.cleaned_data.get('price')
        service.duration = self.cleaned_data.get('duration')
        service.save()
        return service

    def __init__(self, *args, **kwargs):
         self.user = kwargs.pop('user',None)
         super(ServiceForm, self).__init__(*args, **kwargs)

class UpdateServiceForm(forms.ModelForm):
    # type = forms.CharField(max_length=50, required=True)
    # maxCapacity = forms.IntegerField(required=True)
    # price = forms.DecimalField(max_digits=36, decimal_places=2, required=True)

    class Meta:
        model = Service
        fields = ('type', 'maxCapacity', 'price', 'duration')

    # @transaction.atomic
    def save(self):
        service = super().save(commit=False)
        service.type = self.cleaned_data.get('type')
        service.maxCapacity = self.cleaned_data.get('maxCapacity')
        service.price = self.cleaned_data.get('price')
        service.duration = self.cleaned_data.get('duration')
        service.save()
        return service
