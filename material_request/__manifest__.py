# -*- coding: utf-8 -*-
{
    'name': "material request",
    'version': '16.0.1.0.0',
    'summary': 'Material Request',
    'depends': ['base', 'sale_management', 'stock'],
    'author': "Author Name",
    'category': 'Sales',
    'description': """
    Description text
    """,
    'data': [
        'security/security_group.xml',
        'security/ir.model.access.csv',
        'data/material_req_sequence.xml',
        'view/material_request_action.xml',
        'view/material_request.xml',

    ],
    'application': True,

}