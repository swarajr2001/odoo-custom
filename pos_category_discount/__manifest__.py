# -*- coding: utf-8 -*-
{
    'name': "POS category wise discount",
    'version': '16.0.1.0.0',
    'summary':'POS category wise discount',
    'depends': ['base','point_of_sale','pos_sale'],
    'author': "Author Name",
    'category': 'Website',
    'description': """
    give POS category wise discount to product
    """,
    'data': [
            'views/pos_settings_inherited.xml'
    ],
        "assets":{
                "point_of_sale.assets": [
                        'pos_category_discount/static/src/js/discount_limit.js'
                    ],
            },
    'application': True,

}