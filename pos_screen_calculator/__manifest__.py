# -*- coding: utf-8 -*-
{
    'name': "Pos calculator",
    'version': '16.0.1.0.0',
    'summary': 'this is a custom module in which added calculator in pos screen',
    'depends': ['base', 'point_of_sale', 'pos_sale'],
    'author': "Swaaraj R",
    'category': 'Property',
    'description': """
        this is a custom module in which added calculator in pos screen""",
    'data': [

    ],
    "assets": {
        "point_of_sale.assets": [
            'pos_screen_calculator/static/src/xml/calculator_number.xml',
            'pos_screen_calculator/static/src/js/calculator_operation.js',
            'pos_screen_calculator/static/src/xml/pos_calculator.xml',
            'pos_screen_calculator/static/src/js/pos_calculator.js',

        ],
    },
    'application': True,

}
