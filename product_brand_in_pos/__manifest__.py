# -*- coding: utf-8 -*-
{
    'name': "product brand in pos",
    'version': '16.0.1.0.0',
    'summary':'this is a custom module in which added product brand in pos',
    'depends': ['base','point_of_sale','pos_sale'],
    'author': "Swaaraj R",
    'category': 'Property',
    'description': """
        this is a custom module in which added product brand in pos """,
    'data': [
        'views/brand_field_inherited.xml',
    ],
        "assets":{
                "point_of_sale.assets": [
                        'product_brand_in_pos/static/src/xml/*',
                        'product_brand_in_pos/static/src/js/*',
                    ],
            },
    'application': True,

}