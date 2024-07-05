# -*- coding: utf-8 -*-
{
    'name': "Hotel Management System",
    'version': '1.0',
    'category': 'Hotel Management',
    'summary': 'Module for hotel management',
    'description': """
        Long description of module's purpose
    """,
    'author': "DANOUNI Nouhaila",
    'website': "https://www.yourcompany.com",
    'depends': ['base', 'mail'],
    'data': [
        'data/module_category_data.xml',
        'data/cron.xml',
        'data/email_template.xml',
        'security/ir.model.access.csv',
        'views/dashboard_view.xml',
        'views/room_view.xml',
        'views/client_view.xml',
        'views/reservation_view.xml',
        'views/service_view.xml',
        'views/staff_view.xml',
        'report/facture_report.xml',
        'report/facture_report_template.xml',
        'views/confirmation_view.xml',
        'views/shift_view.xml',
        'views/archive.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
