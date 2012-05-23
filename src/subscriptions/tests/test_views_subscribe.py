# coding: utf-8
__author__ = 'Renato'

from django.test import TestCase
from django.core.urlresolvers import reverse, resolve
from ..models import Subscription
from django.db import IntegrityError
from ..forms import SubscriptionForm
from django.core import mail
from django.conf import settings

class SubscribeViewTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(reverse('subscriptions:subscribe'))
        self.form = self.resp.context['form']

    def test_get(self):
        "Ao visitar /inscricao/ a página de inscrição é exibida"
        self.assertEquals(200, self.resp.status_code)

    def test_use_template(self):
        "O corpo da resposta deve conter a renderização de um template"
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        "A resposta deve conter o formulário de inscrição"
        self.assertIsInstance(self.form, SubscriptionForm)

    def test_form_has_fields(self):
        "O formulário deve conter campos: nome, email, cpf e phone"
        #form = self.resp.context['form']
        self.assertItemsEqual(['name', 'email', 'cpf', 'phone'], self.form.fields)

    def test_html(self):
        "O html deve conter os campos do formulário"
        self.assertContains(self.resp, 'form')
        self.assertContains(self.resp, 'input', 6)
        self.assertContains(self.resp, 'type="text"', 4)
        self.assertContains(self.resp, 'submit')

class SubscribeViewsPostTest(TestCase):
    def setUp(self):
        data = dict(name="Renato Lopes", cpf="123456789", email="renatolfilho@gmail.com", phone = "94251041")
        self.resp = self.client.post(reverse('subscriptions:subscribe'), data)

    def test_post(self):
        # Post deve redirecionar para a página de sucesso
        self.assertRedirects(self.resp, reverse('subscriptions:success',args=[1]))

    def test_save(self):
        # Post deve salvar no banco
        self.assertTrue(Subscription.objects.exists())

    def test_email_sent(self):
        # Post deve notificar visitante por email
        self.assertEqual(1, len(mail.outbox))

class SubscribeViewsInvalidPostTest(TestCase):
    def setUp(self):
        data = dict(name="Renato Lopes", cpf="12345678911112", email="renatolfilho@gmail.com", phone = "94251041")
        self.resp = self.client.post(reverse('subscriptions:subscribe'), data)

    def test_show_page(self):
        # Post inválido não deve redirecionar
        self.assertEqual(200, self.resp.status_code)

    def test_form_erros(self):
        # Form deve conter erros
        self.assertTrue(self.resp.context['form'].errors)

    def test_must_not_save(self):
        # Dados não devem ser salvos
        self.assertFalse(Subscription.objects.exists())

    def test_email_not_sent(self):
        # Post deve notificar visitante por email
        self.assertEqual(0, len(mail.outbox))
