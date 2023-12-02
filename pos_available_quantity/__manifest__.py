# -*- coding: utf-8 -*-
{
    'name': "pos available quantity",
    'version': '16.0.1.0.0',
    'summary':'show available warehouse quantity in pos',
    'depends': ['base','point_of_sale','pos_sale'],
    'author': "Swaraj R",
    'category': 'Sales',
    'description': """
    this module showsthe  available warehouse quantity in pos
    """,
    'data': [
    ],
        'assets': {
           'point_of_sale.assets': [
               'pos_available_quantity//static/src/xml/pos_product_card_inherited.xml',
           ],
        },

    'application': True,

}