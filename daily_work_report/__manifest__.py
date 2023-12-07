# -*- coding: utf-8 -*-
{
    'name': "Daily work report tracker",
    'version': '16.0.1.0.0',
    'summary':'Daily work report tracker of employeee',
    'depends': ['base','survey','contacts'],
    'author': "Swaraj R",
    'category': 'Property',
    'description': """
    Daily work report tracker of employeee
    """,

    'data': [
        'security/ir.model.access.csv',
        'views/employee_report.xml',
    ],

    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}