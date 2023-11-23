# -*- coding: utf-8 -*-
{
    "name":"Employee dashboard ",
    'summary': 'this dashboard shows employee details,payslips,leaves,work experience such kind of info',
    "version":"16.0.1.0,0",
    "depends":["base","sale_management",'hr','hr_holidays','project','hr_payroll_community','hr_attendance'],
    'category': 'Property',
    'author': "Swaraj R",
    'description': """
        this dashboard shows employee details,payslips
        leaves,work experience such kind of info
    """,

    'data': [
        'views/menuitem.xml',
    ],

    'assets': {
   'web.assets_backend': [
        'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js',
        'employee_dashboard/static/src/xml/dashboard.xml',
        'employee_dashboard/static/src/js/dashboard.js',
        'employee_dashboard/static/src/css/employee_dashboard.css',
   ],
},

    'application': True,
}