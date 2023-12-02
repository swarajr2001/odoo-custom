# -*- coding: utf-8 -*-
{
    'name': "Migration",
    'version': '16.0.1.0.0',
    'summary':'this custom helps to get product from odoo V15 to V16',
    'depends': ['base','sale_management'],
    'author': "Swaraj",
    'category': 'Sales',
    'description': """
    this custom helps to get product from odoo V15 to V16
    """,
    'data': [
            'security/ir.model.access.csv',
            'views/product_migration_wizard_view.xml',
    ],
    'application': True,

}