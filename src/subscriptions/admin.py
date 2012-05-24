# coding: utf-8
__author__ = 'Renato'

from django.utils.datetime_safe import datetime
from django.contrib import admin
from .models import Subscription
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext
from django.conf.urls import patterns,url
from django.http import HttpResponse

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at', 'subscribed_today', 'paid')
    date_hierarchy = 'created_at'
    search_fields = ('name', 'cpf', 'email', 'phone', 'created_at')
    list_filter = ['created_at','paid']
    actions = ['mark_as_paid']

    #TODO Testar - RequestFactory, subscriptions.object.o (QuerySet)
    def mark_as_paid(self, request, queryset):
        count = queryset.update(paid=True)

        msg = ungettext(
            u'%(count)d inscrição foi marcada como paga.',
            u'%(count)d inscrições foram marcadas como pagas.',
            count
        ) % {'count':count}

        self.message_user(request, msg)
    mark_as_paid.short_description = _(u"Marcar como pagas")

    def subscribed_today(self, obj):
        return obj.created_at.date() == datetime.today().date()
    subscribed_today.short_description = u"Inscrito Hoje?"
    subscribed_today.boolean = True

    def export_subscriptions(self,request):
        subscriptions = self.model.objects.all()
        rows = [','.join([s.name,s.email]) for s in subscriptions]

        response = HttpResponse('\r\n'.join(rows))
        response.mimeType = 'text/csv'
        response['Content-Disposition'] = 'attachment; filename=inscricoes.csv'
        return response

    #TODO Testar get nessa view
    def get_urls(self):
        original_urls = super(SubscriptionAdmin, self).get_urls()
        extra_url = patterns('',
            # Envolve nossa view em 'admin_view' por que ela faz o
            # controle de permissões e cache automaticamente para nós
            url(r'exportar-inscricoes/$',
                self.admin_site.admin_view(self.export_subscriptions),
                name='export_subscriptions')
        )
        # A ordem é importante. As urls originais do admin são muito permissivas
        # e acabam sendo encontradas antes da nossa se elas estiverem na frente
        return extra_url + original_urls

admin.site.register(Subscription, SubscriptionAdmin)
