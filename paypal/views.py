# -*- coding: utf-8 -*-

import urllib
from django.http import Http404, HttpResponse
from django.views.generic.simple import direct_to_template
from livesettings import config_get_group
from paypal.processor import PaymentProcessor
from paypal import settings

PROCESSOR_KEY = 'PAYMENT_PAYPAL'

def payment_return(request):
    token = request.GET.get('token')
    payer_id = request.GET.get('PayerID')

    if not token and not payer_id:
        raise Http404

    processor = PaymentProcessor(config_get_group(PROCESSOR_KEY))
    processor.capture_payment(token, payer_id)

    return direct_to_template(request, 'shop/checkout/payment_return.html')

def ipn(request):
    params = {'cmd': '_notify-validate'}

    for k, v in request.POST.items():
        params[k] = v.encode('utf-8')

    response = urllib.urlopen(settings.IPN_ENDPOINT,
        urllib.urlencode(params)).read()

    if response == 'VERIFIED':
        processor = PaymentProcessor(config_get_group(PROCESSOR_KEY))
        processor.update_payment(request.POST)

        return HttpResponse('OK')

    raise Http404
