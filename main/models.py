from django.db import models
from register.models import User, Partner
import datetime
from pytz import timezone
# Create your models here.

class Service(models.Model):
    """
    This model contains information about the service being provided.
    PK: Business Partner, Service Type.
    A business partner can provide many kind of services (e.g., a salon can provide haircut, pati&mani etc.)
    So the combination of the business partner and the service type determines a single service.
    :Business_Partner: Connection to register app's User model.
    :Type: Type of service.
    :Max_Capacity: How many such kind of service can the business partner produce at a certain time slot.
    :price: Price of the service.
    """
    businessPartner = models.ForeignKey(
            Partner,
            blank=False,
            null=False,
            on_delete=models.CASCADE
    )
    type = models.CharField(max_length=50, blank=False, null=False)
    maxCapacity = models.IntegerField(blank=False, default=1)
    price = models.DecimalField(max_digits=36, decimal_places=2, blank=False, null=False)

    DURATION = [
        (30, '30 Minutes'),
        (60, '1 Hour'),
        (90, '1.5 Hour'),
        (120, '2 Hour'),
        (180, '3 Hour')
    ]

    duration = models.IntegerField(blank=False, choices=DURATION, default=60)

    class Meta:
        unique_together = (("businessPartner", "type"), )

    def __str__(self):
        return '{} by {}'.format(self.type, self.businessPartner)

# class TimeSlot(models.Model):
#     """
#     This model contains information about the time slot.
#     PK: Business Partner, Service Type
#     Each service of every business partner has one time slot table contains date and time.
#     This is connected to service model, it only appears when a service being created.
#     :Service_Type: Foreign key, connection to service model.
#     :date: Date of the time slot.
#     :startTime: Starting time of the time slot.
#     :endTime: Ending time of the time slot.
#     """
#     # serviceType = models.OneToOneField(
#     #         Service,
#     #         blank=False,
#     #         null=False,
#     #         on_delete=models.CASCADE,
#     #         primary_key=True
#     # )
#     date = models.DateField()
#     startTime = models.TimeField()
#     endTime = models.TimeField()

class Appointment(models.Model):
    """
    This model contains information about the booking of a service at a certain time.
    PK: Business Partner, Service Type, Time Slot.
    Meaning that the combination of a business, a service and a certain time slot determines
    a single booking.
    :timeSlot: Foreign key inherited from TimeSlot model.
    :status: Current status of the booking.
    :creation_date: The time when the Appointment has been made (potentionally use for notification)
    """
    customer = models.ForeignKey(User, limit_choices_to={'isUser': True}, on_delete=models.DO_NOTHING)
    partner = models.ForeignKey(Partner, on_delete=models.DO_NOTHING)
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING)
    # timeSlot = models.OneToOneField(TimeSlot, on_delete=models.PROTECT)
    STATUS = [
        ('BOOKED', 'Booked'),
        ('CANCELLED', 'Cancelled')
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='BOOKED')
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    creationTime = models.DateTimeField(auto_now_add=True)

    @property
    def is_complete(self):
        if datetime.datetime.now() > self.endTime.astimezone(timezone('America/Chicago')).replace(tzinfo=None):
            return True
        return False

    def __str__(self):
        return '{}-{}-{}'.format(self.customer, self.partner, self.service)
