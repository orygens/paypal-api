# -*- coding: utf-8 -*-

from django.conf import settings

RETURN_URL = getattr(settings, 'PAYPAL_RETURN_URL', None)
CANCEL_URL = getattr(settings, 'PAYPAL_CANCEL_URL', None)
CURRENCY_CODE = getattr(settings, 'PAYPAL_CURRENCY_CODE', 'BRL')
RECEIVER_EMAIL = getattr(settings, 'PAYPAL_RECEIVER_EMAIL', None)
USER = getattr(settings, 'PAYPAL_USER', None)
PASSWORD = getattr(settings, 'PAYPAL_PASSWORD')
SIGNATURE = getattr(settings, 'PAYPAL_SIGNATURE')
ENDPOINT = getattr(settings, 'PAYPAL_ENDPOINT',
    'https://api-3t.sandbox.paypal.com/nvp')
IPN_ENDPOINT = getattr(settings, 'PAYPAL_IPN_ENDPOINT',
    'https://www.sandbox.paypal.com/cgi-bin/webscr')
POST_URL = getattr(settings, 'PAYPAL_POST_URL',
    'https://www.sandbox.paypal.com/webscr')
VERSION = getattr(settings, 'PAYPAL_VERSION', '83.0')
