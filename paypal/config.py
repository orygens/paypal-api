# -*- coding: utf-8 -*-

import settings
from livesettings import *

PAYMENT_GROUP = ConfigurationGroup('PAYMENT_PAYPAL',
    'PayPal Payment Module Settings',
    ordering=101
)

config_register_list(
    StringValue(PAYMENT_GROUP,
        'CURRENCY_CODE',
        description='Currency code',
        help_text='Currency code for PayPal transactions',
        default=settings.CURRENCY_CODE
    ),
    StringValue(PAYMENT_GROUP,
        'POST_URL',
        description='Post URL',
        help_text='The PayPal URL for transactional posting.',
        default=settings.POST_URL
    ),
    StringValue(PAYMENT_GROUP,
        'USER',
        description='User',
        help_text='The PayPal seller user.',
        default=settings.USER
    ),
    StringValue(PAYMENT_GROUP,
        'PASSWORD',
        description='Password',
        help_text='The PayPal seller API password.',
        default=settings.PASSWORD
    ),
    StringValue(PAYMENT_GROUP,
        'SIGNATURE',
        description='Signature',
        help_text='The PayPal seller API signature.',
        default=settings.SIGNATURE
    ),
    StringValue(PAYMENT_GROUP,
        'VERSION',
        description='Version',
        help_text='The PayPal API version.',
        default=settings.VERSION
    ),
    StringValue(PAYMENT_GROUP,
        'RETURN_URL',
        description='Return URL',
        help_text='Where Paypal will return the customer after the purchase ' +\
            'is complete.  This can be a named url and defaults to the ' +\
            'standard checkout success.',
        default=settings.RETURN_URL
    ),
    StringValue(PAYMENT_GROUP,
        'CANCEL_URL',
        description='Cancel URL',
        help_text='Where Paypal will return the customer after the purchase ' +\
            'is canceled.  This can be a named url.',
        default=settings.CANCEL_URL
    ),
    ModuleValue(PAYMENT_GROUP,
        'MODULE',
        description='Implementation module',
        hidden=True,
        default = 'apps.paypal'
    ),
    StringValue(PAYMENT_GROUP,
        'KEY',
        description='Module key',
        hidden=True,
        default ='PAYPAL'
    ),
    StringValue(PAYMENT_GROUP,
        'LABEL',
        description='Name for this group on the checkout screens',
        default='PayPal',
        help_text='PayPal'
    ),
    StringValue(PAYMENT_GROUP,
        'URL_BASE',
        description='The url base used for constructing urlpatterns which ' +\
            'will use this module',
        default='^paypal/'
    ),
    BooleanValue(PAYMENT_GROUP,
        'EXTRA_LOGGING',
        description='Verbose logs',
        help_text='Add extensive logs during post.',
        default=False
    )
)

PAYMENT_GROUP['TEMPLATE_OVERRIDES'] = {
    'shop/checkout/success.html' : 'shop/checkout/payment_redirect.html',
}
