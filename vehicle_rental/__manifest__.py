# -*- coding: utf-8 -*-
{
    'name': "Vehicle Rental",
    'version': '16.0.1.0.0',
    'summary':'Vechicle Rental management system',
    'depends': ['base','fleet','account','website'],
    'author': "Author Name",
    'category': 'Property',
    'description': """
    Description text
    """,

    'data': [
        'security/security_group.xml',
        'security/ir.model.access.csv',
        'security/own_doccument.xml',
        'view/vehicle_details_view.xml',
        'view/vehicle_request_view.xml',
        'data/vehicle_request_sequence.xml',
        'view/fleet_vehicle_view.xml',
        'view/schedule_action.xml',
        'report/vehicle_request_report.xml',
        'view/vehicle_actions.xml',
        'report/vehicle_report_template.xml',
        'report/vehicle_request_report_action.xml',
        'data/vehicle_request_menu.xml',
        'vehicle_rental_website/views/vehicle_rental_website.xml',
        'vehicle_rental_website/views/rental_request_success.xml',
        'vehicle_rental_website/views/vehicle_rental_website_tree.xml',
        'vehicle_rental_website/views/add_customer.xml',
        'vehicle_rental_website/views/rental_request_view.xml',
        'vehicle_rental_website/views/vehicle_rental_snippet.xml',
        'vehicle_rental_website/views/vehicle_view.xml',
    ],
        "assets":{
                "web.assets_backend": [
                        'vehicle_rental/static/src/js/action_manager.js',
                    ],
                "web.assets_frontend": [
                        'vehicle_rental/static/src/js/vehicle_request_snippet.js',
                        'vehicle_rental/static/src/js/vehicle_request.js',
                        'vehicle_rental/static/src/xml/*',

                    ],
            },
    'application': True,

}