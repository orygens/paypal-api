# -*- coding: utf-8 -*-

# Essas duas linhas são usadas pelo Satchmo
import config
PAYMENT_PROCESSOR=True

from django.db import models
from django.db.models.signals import pre_save, post_save
from checkout.models import Payment, psave_payment, check_for_offer_purchase

class PayPalPayment(Payment):
    TRANSACTION_STATUS_CHOICES = [
        (0, 'Canceled_Reversal'),
        (1, 'Completed'),
        (2, 'Created'),
        (3, 'Denied'),
        (4, 'Expired'),
        (5, 'Failed'),
        (6, 'Pending'),
        (7, 'Refunded'),
        (8, 'Reversed'),
        (9, 'Processed'),
        (10, 'Voided')
    ]
    TRANSLATED_STATUS_CHOICES = {
        0: 'Retorno cancelado',
        1: 'Completado',
        2: 'Criado',
        3: 'Negado pelo vendedor',
        4: u'Autorização expirada',
        5: 'Falhou',
        6: 'Pendente',
        7: 'Reembolsado pelo vendedor',
        8: 'Retornado',
        9: 'Aceito',
        10: 'Voided'
    }
    AUTHORIZED_STATUSES = [1]
    CANCELED_STATUSES = [3, 4, 5, 7, 8, 0]

    token = models.CharField('token', max_length=60, blank=True, null=True)
    payer_id = models.CharField('token', max_length=60, blank=True, null=True)
    transaction_status = models.IntegerField(u'status da transação',
        choices=TRANSACTION_STATUS_CHOICES, default=2)
    transaction_id = models.CharField(u'id da transação', max_length=60,
        blank=True, null=True)

    def save(self, *args, **kwargs):
        self.transaction_source = 3
        super(PayPalPayment, self).save(*args, **kwargs)

    @property
    def transaction_statuses(self):
        if not getattr(self, '_transaction_statuses', None):
            self._transaction_statuses = dict(map(lambda (a, b): (b, a),
                PayPalPayment.TRANSACTION_STATUS_CHOICES))

        return self._transaction_statuses

    def get_status_text(self):
        return PayPalPayment.TRANSLATED_STATUS_CHOICES[self.transaction_status]
    status_text = property(get_status_text)

def paypal_pre_save(sender, instance, **kwargs):
    return psave_payment(sender, instance,
        PayPalPayment.AUTHORIZED_STATUSES, **kwargs)

pre_save.connect(paypal_pre_save, PayPalPayment)
post_save.connect(check_for_offer_purchase, PayPalPayment)
