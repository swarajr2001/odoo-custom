# -*- coding: utf-8 -*-

from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleControllerInherited(WebsiteSale):

    def _get_shop_payment_values(self, order, **kwargs):
        values = super()._get_shop_payment_values(order)
        template = request.env.ref('website_pay_mail.website_email_manager')
        email_values = {
            'subject': f'Assignment of online orders {order.name} to your sales team',
        }
        email_values['email_to'] = order.team_id.user_id.email or order.user_id.login
        template.send_mail(order.id, email_values=email_values, force_send=True)
        return values
