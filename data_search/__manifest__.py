# -*- coding: utf-8 -*-
{
    'name': "Data search",
    'version': '16.0.1.0.0',
    'summary':'this custom app that search specified data from all odoo models',
    'depends': ['base'],
    'author': "Swaraj R",
    'category': 'Property',
    'description': """
    this custom app that search specified data from all odoo models
    """,

    'data': [
        'security/ir.model.access.csv',
        'views/data_search.xml',
    ],


    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}