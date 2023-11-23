# -*- coding: utf-8 -*-

import time, urllib

from werkzeug import urls

from odoo import _, models, api
from odoo.exceptions import ValidationError

from odoo.addons.payment import utils as payment_utils
from odoo.addons.payment_provider_payu.controllers.main import PayUController


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        """this function renders values to the template"""
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'payu':
            return res
        apiEndpoint = "https://test.payu.in/_payment"
        txnId = "TXN" + str(int(time.time()))
        first_name, last_name = payment_utils.split_partner_name(self.partner_id.name)
        key = self.provider_id.merchant_key
        print(key)
        amount = str(self.amount)
        productinfo = self.reference
        email = self.partner_email
        phone = self.partner_phone
        payload = {
            "key": key,
            "txnid": txnId,
            "amount": amount,
            "productinfo": productinfo,
            "firstname": first_name,
            "lastname": first_name,
            "email": email,
            "phone": phone,
            'return_url': urls.url_join(self.get_base_url(), PayUController._return_url),
        }
        payload['hash'] = self.provider_id._payu_generate_sign(
            payload, incoming=False,
        )
        print(payload['hash'],"trans-hash")
        encodedParams = urllib.parse.urlencode(payload)
        url = apiEndpoint + "?" + encodedParams
        payload['api_url'] = url
        print(payload)
        return payload

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """function returns suitable notification message of the transaction"""
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'payu' or len(tx) == 1:
            return tx
        reference = notification_data.get('productinfo')
        if not reference:
            raise ValidationError(
                "PayU: " + _("Received data with missing reference (%s)", reference)
            )
        tx = self.search([('reference', '=', reference), ('provider_code', '=', 'payu')])
        if not tx:
            raise ValidationError(
                "PayU: " + _("No transaction found matching reference %s.", reference)
            )
        return tx

    def _process_notification_data(self, notification_data):
        """function that process the notification"""
        super()._process_notification_data(notification_data)
        if self.provider_code != 'payu':
            return
        status = notification_data.get('status')
        self.provider_reference = notification_data.get('payuMoneyId')
        if status == 'success':
            self._set_done()
        else:
            error_code = notification_data.get('error_Message')
            self._set_error(
                "PayU: " + _("The payment encountered an error with code %s", error_code)
            )
