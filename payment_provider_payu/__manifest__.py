# -*- coding: utf-8 -*-
{
    'name': 'Payment Provider: Payu',
    'version': '16.0.0.1',
    'category': 'Accounting/Payment Providers',
    'sequence': 355,
    'summary': "PayU provides payment gateway solutions to online businesses through its cutting-edge and award-winning technolog.",
    'depends': ['payment'],
    'data': [
            'views/payu_template.xml',
            'views/payment_payu.xml',
            'data/payu_payment_data.xml',
            'data/automatic_invoice.xml'

    ],

}