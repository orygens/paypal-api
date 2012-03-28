# -*- coding: utf-8 -*-

import urllib
from django.core.exceptions import ImproperlyConfigured
from paypal import settings
from cgi import parse_qs

class API(object):
    required_settings = [
        'RETURN_URL',
        'CANCEL_URL',
        'USER',
        'PASSWORD',
        'SIGNATURE',
        'VERSION'
    ]

    def __init__(self, **kwargs):
        for setting in self.required_settings:
            setting_value = getattr(settings, setting)

            if not setting_value:
                raise ImproperlyConfigured,\
                    "You've forgot to set the PAYPAL_%s setting." % setting

            setattr(self, setting.lower(), setting_value)

        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def auth(self):
        if not getattr(self, '_auth', None):
            self._auth = {
                'USER': self.user,
                'PWD': self.password,
                'SIGNATURE': self.signature,
                'VERSION': self.version,
                'PAYMENTREQUEST_0_CURRENCYCODE': settings.CURRENCY_CODE
            }

        return self._auth

    def set_express_checkout(self, amount, **kwargs):
        params = {
            'METHOD' : 'SetExpressCheckout',
            'NOSHIPPING' : 1,
            'RETURNURL' : self.return_url,
            'CANCELURL' : self.cancel_url,
            'PAYMENTREQUEST_0_AMT' : amount,
            'PAYMENTREQUEST_0_PAYMENTACTION': 'Sale',
        }
        params.update(self.auth)
        params.update(kwargs)
        params_string = urllib.urlencode(params)
        response = urllib.urlopen(settings.ENDPOINT, params_string).read()

        return parse_qs(response)['TOKEN'][0]

    def do_express_checkout_payment(self, amount, token, payer_id, **kwargs):
        params = {
            'METHOD': 'DoExpressCheckoutPayment',
            'PAYERID': payer_id,
            'TOKEN': token,
            'PAYMENTREQUEST_0_AMT': amount,
            'PAYMENTREQUEST_0_PAYMENTACTION': 'Sale',
        }
        params.update(self.auth)
        params.update(kwargs)
        params_string = urllib.urlencode(params)
        response = urllib.urlopen(settings.ENDPOINT, params_string).read()

        return parse_qs(response)
