# coding: utf-8
from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from .forms import SubscriptionForm
from django.core.mail import send_mail
from django.conf import settings
from .models import Subscription
from django.shortcuts import get_object_or_404

def subscribe(request):
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)


def new(request):
    return direct_to_template(request, 'subscriptions/subscription_form.html', {'form': SubscriptionForm()})

def create(request):
    form = SubscriptionForm(request.POST)

    if not form.is_valid():
        return direct_to_template(request, 'subscriptions/subscription_form.html', {'form': form})

    subscription = form.save()
    send_mail(subject=u"Cadastrado com Sucesso",
                message=u"Obrigado pela sua inscrição",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[subscription.email])


    return HttpResponseRedirect(reverse('subscriptions:success',
                                args=[subscription.pk]))

def success(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk)
    return direct_to_template(request, "subscriptions/subscription_detail.html", { 'subscription': subscription})