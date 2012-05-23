# coding: utf-8
__author__ = 'Renato'

from django.test import TestCase
from django.core.urlresolvers import reverse, resolve
from ..models import Subscription
from django.conf import settings

class SucessViewTest(TestCase):
    def setUp(self):
        s = Subscription.objects.create(name="Renato Lopes", cpf="123456789", email = "renatolfilho@gmail.com", phone="94251041")
        self.resp = self.client.get(reverse('subscriptions:success', args=[s.pk]))

    # Visita a página de sucesso
    def test_get(self):
        self.assertEquals(200, self.resp.status_code)

    # Verifica template
    def test_use_template(self):
        self.assertTemplateUsed(self.resp, "subscriptions/subscription_detail.html")

    def test_context(self):
        subscription = self.resp.context['subscription']
        self.assertIsInstance(subscription, Subscription)

    def test_html(self):
        self.assertNotContains(self.resp, settings.TEMPLATE_STRING_IF_INVALID)

class SuccessViewNotFound:
    def test_not_found(self):
        response = self.client.get(reverse("subscribe:success", args[0]))
        self.assertEquals(404, response.status_code)
