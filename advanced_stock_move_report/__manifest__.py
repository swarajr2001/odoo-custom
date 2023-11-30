# -*- coding: utf-8 -*-
{
    'name': "advanced stock move report",
    'version': '16.0.1.0.0',
    'summary':'this custom app generates the advanced stock move report',
    'depends': ['base','sale_management','stock'],
    'author': "Swaraj R",
    'category': 'Property',
    'description': """
    this custom app generates the advanced stock move report
    """,

    'data': [
        'security/ir.model.access.csv',
        'report/stock_report_template.xml',
        'report/stock_move_report_action.xml',
        'report/stock_report_wizard.xml',
    ],

    "assets": {
        "web.assets_backend": [
            'advanced_stock_move_report/static/src/js/action_manager.js',
        ],
    },

    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}