# -*- coding: utf-8 -*-

from django.utils.html import strip_tags
from payment.modules.base import BasePaymentProcessor
from paypal.api import API
from paypal.models import PayPalPayment
from paypal import settings
from checkout.emails import PaymentStatusEmailHelper
from emailconfirmation.models import EmailAddress
from orygens_utils.templatetags.string_tags import smart_truncate_words

class PaymentProcessor(BasePaymentProcessor):
    def __init__(self, settings):
        super(PaymentProcessor, self).__init__('paypal', settings)
        self.data = {}
        self.return_url = settings.RETURN_URL.value
        self.cancel_url = settings.CANCEL_URL.value
        self.user = settings.USER.value
        self.password = settings.PASSWORD.value
        self.signature = settings.SIGNATURE.value
        self.version = settings.VERSION.value
        self.post_url = settings.POST_URL.value

    @property
    def api(self):
        if not getattr(self, '_api', None):
            self._api = API(
                return_url=self.return_url,
                cancel_url=self.cancel_url,
                user=self.user,
                password=self.password,
                signature=self.signature,
                version=self.version
            )

        return self._api

    def prepare_data(self, order):
        profile = order.contact.user.store_profile
        email = EmailAddress.objects.get_primary(profile.user).email or\
            EmailAddress.objects.filter(user=profile.user)[0].email
        self.order = order
        amount = float(max(order.total - (order.discount or 0), 0))
        kwargs = {
            'PAYMENTREQUEST_0_ITEMAMT': amount,
            'PAYMENTREQUEST_0_EMAIL': email,
            'PAYMENTREQUEST_0_SHIPTOCPF': profile.cpf,
            'PAYMENTREQUEST_0_SHIPTONAME': profile.fullname.encode('utf-8'),
            'PAYMENTREQUEST_0_SHIPTOSTREET': profile.address.encode('utf-8'),
            'PAYMENTREQUEST_0_SHIPTOSTREET2': profile.district.encode('utf-8'),
            'PAYMENTREQUEST_0_SHIPTOCITY': profile.city.encode('utf-8'),
            'PAYMENTREQUEST_0_SHIPTOSTATE': profile.state.name.encode('utf-8'),
            'PAYMENTREQUEST_0_SHIPTOCOUNTRYCODE': 'BR',
            'PAYMENTREQUEST_0_SHIPTOZIP': profile.zip_code,
            'PAYMENTREQUEST_0_SHIPTOPHONENUM': profile.phone_number1
        }

        for i, item in enumerate(order.orderitem_set.all()):
            product = item.product
            kwargs.update({
                'L_PAYMENTREQUEST_0_NAME%d' % i: product.name.encode('utf-8'),
                'L_PAYMENTREQUEST_0_DESC%d' % i:
                    smart_truncate_words(strip_tags(product.description).encode('utf-8'), 96) or\
                    u'Descrição não informada',
                'L_PAYMENTREQUEST_0_AMT%d' % i: float(product.unit_price),
                'L_PAYMENTREQUEST_0_QTY%d' % i: int(item.quantity)
            })

        if order.discount != None and order.discount > 0:
            i = i + 1
            kwargs.update({
                'L_PAYMENTREQUEST_0_NAME%d' % i: 'Desconto',
                'L_PAYMENTREQUEST_0_AMT%d' % i: order.discount * (-1)
            })

        self.data['token'] = self.api.set_express_checkout(amount, **kwargs)
        self.data['cmd'] = '_express-checkout'
        PayPalPayment.objects.get_or_create(
            order=self.order,
            token=self.data['token']
        )

    def capture_payment(self, token, payer_id):
        payment = PayPalPayment.objects.get(token=token)
        order = payment.order
        amount = float(max(order.total- (order.discount or 0), 0))
        response = self.api.do_express_checkout_payment(amount, token, payer_id)
        payment.payer_id = payer_id
        status = response['PAYMENTINFO_0_PAYMENTSTATUS'][0]
        payment.transaction_status = payment.transaction_statuses[status]
        payment.transaction_id = response['PAYMENTINFO_0_TRANSACTIONID'][0]
        payment.save()
        self._post_process_payment(payment)

    def update_payment(self, data):
        payment = PayPalPayment.objects.get(transaction_id=data['txn_id'])
        new_status = payment.transaction_statuses[data['payment_status']]

        if payment.transaction_status != new_status and settings.RECEIVER_EMAIL == data['receiver_email']:
            payment.transaction_status = new_status
            payment.save()
            self._post_process_payment(payment)

    def _post_process_payment(self, payment):
        if payment.transaction_status in PayPalPayment.AUTHORIZED_STATUSES:
            order = payment.order
            self.record_payment(order=order, amount=order.balance,
                transaction_id='paypal', reason_code=0)
            PaymentStatusEmailHelper.payment_status_notification(
                order.contact.user, payment)
