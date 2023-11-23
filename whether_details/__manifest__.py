# -*- coding: utf-8 -*-
{
    "name":"whether system ",
    'summary': 'weather update system',
    "version":"16.0.1.0,0",
    "depends":["web"],
    'category': 'Property',
    'author': "Swaraj R",
    'description': """
        custom weather icon in systray
    """,

    'data': [
            'views/res_config_setting_inherited.xml',
    ],

    "assets":{
        "web.assets_backend": [
            "/whether_details/static/src/js/whether.js",
            "/whether_details/static/src/xml/whether.xml"
        ]
    },
    'application': True,
}
