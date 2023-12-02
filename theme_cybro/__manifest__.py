# -*- coding: utf-8 -*-
{
    'name': "Cybro theme",
    'version': '16.0.1.0.0',
    'summary': 'theme cybros',
    'depends': ['website'],
    'author': "Author Name",
    'category': 'Theme',
    'description': """
    Description text:
    """,

    'data': [
        'data/pages/about_us.xml',
        'data/menu.xml',
    ],

    "assets":{
    'web._assets_primary_variables': [
        '/theme_cybro/static/scss/primary_variables.scss',
        ],
    },

    'images': [
        'static/description/clean_description.jpg',
        'static/description/clean_screenshot.jpg',
    ],

    'application': True,
    'installable': True,
}
