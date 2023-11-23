# -*- coding: utf-8 -*-
{
    'name': "Contact creation from survey",
    'version': '16.0.1.0.0',
    'summary':'Contact creation from survey by filling up data in survey',
    'depends': ['base','survey','contacts'],
    'author': "Swaraj R",
    'category': 'Property',
    'description': """
    Contact creation from survey by filling up data in survey
    """,

    'data': [
        'views/survey_survey_inherited.xml',
        'security/ir.model.access.csv',
    ],

    'application': True,

}