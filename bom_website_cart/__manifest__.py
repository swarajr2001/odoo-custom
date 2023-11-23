# -*- coding: utf-8 -*-
{
    'name': "BOM in website cart",
    'version': '16.0.1.0.0',
    'summary':'when product with bom is added to cart its components will be shown in the description',
    'depends': ['base','website','website_sale'],
    'author': "Swaaraj R",
    'category': 'Property',
    'description': """
    when product with bom is added to cart its components will be shown in the description
    """,
    'data': [
        'views/website_settings_inherited_field.xml',
        'views/website_sale_cart_inherited.xml',
    ],

    'application': True,

}