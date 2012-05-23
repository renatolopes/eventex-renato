# coding: utf-8
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.urlresolvers import reverse, resolve
from ..models import Subscription
from django.db import IntegrityError
from ..forms import SubscriptionForm
from django.core import mail
from django.conf import settings

from .test_urls import  *
from .test_models import  *
from .test_views_subscribe import *
from .test_views_success import *