# coding: utf-8
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.urlresolvers import reverse, resolve
from .models import Subscription
from django.db import IntegrityError

class SubscriptionsUrlTest(TestCase):
    def test_get_subscribe_page(self):
        url = reverse('subscriptions:subscribe')
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)

    def test_get_success_page(self):
        url = reverse('subscriptions:success', args=[1])
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)

class SubscriptionModelTest(TestCase):
    # 1) o modelo deve ter os campos: name, cpf, email, phone, create_at
    def test_create(self):
        s = Subscription.objects.create(
            name='Renato Lopes',
            cpf='12862577700',
            email="renatolfilho@gmail.com",
            phone='21-96186180'
        )

        self.assertEquals(s.id,1)

class SubscriptionModelUniqueTest(TestCase):
    def setUp(self):
        #1) Cria uma primeira inscrição no banco
        Subscription.objects.create( name='Renato Lopes',
            cpf='12862577700',
            email="renatolfilho@gmail.com",
            phone='21-96186180')

    # 2) O cpf deve ser único
    def test_cpf_must_be_unique(self):
        # Instancia a inscrição com CPF existente
        s =  Subscription(name='Renato Lopes',
        cpf='12862577700',
        email="outroemail@email.com",
        phone='21-96186180')

        # Verifica se ocorre o erro de integridade ao persistir
        self.assertRaises(IntegrityError, s.save)

    # 3) O email deve ser único
    def test_email_must_be_unique(self):
        # Instancia a inscrição com Email existente
        s =  Subscription(name='Renato Lopes',
            cpf='00000000000',
            email="renatolfilho@gmail.com",
            phone='21-96186180')

        # Verifica se ocorre o erro de integridade ao persistir
        self.assertRaises(IntegrityError, s.save)