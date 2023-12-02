# -*- coding: utf-8 -*-
{
    'name': "Website pay mail",
    'version': '16.0.1.0.0',
    'summary':'this custom app that If a customer buy from shop, send an email to the sales managers with the corresponding data',
    'depends': ['base','mail','contacts','website','website_sale'],
    'author': "Swaraj R",
    'category': 'Property',
    'description': """
    this custom app that If a customer buy from shop,
     send an email to the sales managers with the corresponding data
    """,

    'data': [
        'data/email_template.xml',
    ],

    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}