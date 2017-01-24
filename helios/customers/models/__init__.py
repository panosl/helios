# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings



class BaseCustomer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True)

    class Meta:
        abstract = True



User.customer = property(lambda u: Customer.objects.get_or_create(
    user=u, defaults={'country': Country.objects.get(pk=1)})[0])
