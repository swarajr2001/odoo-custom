# -*- coding: utf-8 -*-
{
    'name': "sales discount",
    'version': '16.0.1.0.0',
    'summary':'sales discount app',
    'depends': ['base','sale_management'],
    'author': "Author Name",
    'category': 'Property',
    'description': """
    Description text
    """,

    'data': [
            'views/discount_in_order_line.xml',
            'views/discount_in_sale_order.xml',
    ],
    'application': True,
}