# -*- coding: utf-8 -*-
{
    'name': "sales automation",
    'version': '16.0.1.0.0',
    'summary':'Sale Order Automation',
    'depends': ['base','sale_management'], 
    'author': "Author Name",
    'category': 'Property',
    'description': """
    Description text
    """,
    'data': [

        'security/ir.model.access.csv',
        'view/wizard_view.xml',
        'view/sales_inherited.xml',

    ],
    'application': True,

}