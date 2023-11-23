# -*- coding: utf-8 -*-
{
    'name': "tolerance",
    'version': '16.0.1.0.0',
    'summary':'tolerance app',
    'depends': ['base','sale_management','purchase','stock'],
    'author': "Author Name",
    'category': 'Property',
    'description': """
    Description text
    """,
    'data': [
    'security/ir.model.access.csv',
    'views/tolerance_field_added.xml',
    'views/tolerance_in_order_line.xml',
    'views/tolerance_in_stockPicking.xml',
    'views/stock_picking_wizard.xml'

    ],
    'application': True,
}