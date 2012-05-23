# coding: utf-8
__author__ = 'Renato'

from django.test import TestCase
from django.core.urlresolvers import reverse, resolve
from ..models import Subscription
from django.db import IntegrityError
from ..forms import SubscriptionForm

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