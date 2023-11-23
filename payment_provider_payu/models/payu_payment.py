# -*- coding: utf-8 -*-

from odoo import fields, models
import hashlib


class PaymentProvider(models.Model):
    """inherited the payment.provider and added  custom field """
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('payu', "Payu")], ondelete={'payu': 'set default'})
    merchant_key = fields.Char(string="merchant key")
    merchant_salt = fields.Char(string="merchant salt code")

    def _payu_generate_sign(self, values, incoming=True):
        """function 2 calculate the hash code of the transaction this function is invoked from controllers.main
        _verify_notification_signature and models.payu_payment_transaction.py._get_specific_rendering_values"""
        sign_values = {
            **values,
            'key': self.merchant_key,
            'salt': self.merchant_salt,
        }
        if incoming:  # hash calculated for function call from controller function
            print("checking hash")
            keys = 'salt|status||||||udf5|udf4|udf3|udf2|udf1|email|firstname|productinfo|amount|txnid|key'
            sign = '|'.join(f'{sign_values.get(k) or ""}' for k in keys.split('|'))
        else:  # hash calculated from the payment.transaction function
            keys = 'key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5||||||salt'
            sign = '|'.join(f'{sign_values.get(k) or ""}' for k in keys.split('|'))
        return hashlib.sha512(sign.encode('utf-8')).hexdigest()


