# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url
from satchmo_store.shop.satchmo_settings import get_satchmo_setting
from checkout.views import payment

ssl = get_satchmo_setting('SSL', default_value=False)

urlpatterns = patterns('',
    (r'^realizar-pagamento/$', payment,
        {'SSL': ssl, 'processor_key': 'PAYMENT_PAYPAL'},
        'PAYPAL_satchmo_checkout-step3'),
    url(r'^pagamento-efetuado/$', 'paypal.views.payment_return',
        name='paypal_payment_return_path'),
    (r'^ipn/$', 'paypal.views.ipn'),
)
