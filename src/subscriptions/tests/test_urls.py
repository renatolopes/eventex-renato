# coding: utf-8
__author__ = 'Renato'

from django.test import TestCase
from django.core.urlresolvers import reverse, resolve

class SubscriptionsUrlTest(TestCase):
    def test_get_subscribe_page(self):
        url = reverse('subscriptions:subscribe')
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)

    def test_get_success_page(self):
        url = reverse('subscriptions:success', args=[1])
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)