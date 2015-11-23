from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User
from django.contrib.postgres.fields import DateRangeField, IntegerRangeField, ArrayField, HStoreField


class SolarPanel(models.Model):
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="stub", verbose_name=("user"))
    square_feet_access = IntegerRangeField()
    avail_team_period = DateRangeField()  #as opposed to start and stop date which previously used
    types_of_surface = ArrayField(models.CharField(max_length=100, blank=True), 
                       blank = True,
                       null = True,
                     )
    unique_install_parameters = HStoreField()