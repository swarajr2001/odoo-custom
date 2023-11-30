# -*- coding: utf-8 -*-
{
    'name': "sales report monthly weekly",
    'version': '16.0.1.0.0',
    'summary':'Generate custom sales report monthly weekly',
    'depends': ['base','sale_management','mail','contacts'],
    'author': "Author Name",
    'category': 'Property',
    'description': """
    Generate custom sales report monthly weekly basis
    """,
    'data': [
    'data/sales_report_recurrence.xml',
    'security/ir.model.access.csv',
    'report/report_template.xml',
    'report/sales_report_action.xml',
    'data/sales_report_sequence.xml',
    'views/sales_report_view.xml',
    'data/sales_report_email_template.xml',

    ],
    'application': True,
}