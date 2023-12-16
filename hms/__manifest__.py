# -*- coding: utf-8 -*-
{
    'name': "My First Hospital",

    'summary': """
    This Is Hospital Management System Module """,

    'description': """This modeule explain how does hospital manage patients affairs and difference specializations.""",

    'author': "Abdullah Elshoura",
    'website': "abdullah@test.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'crm','sale'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/main_menu_items.xml',
        'views/patient_view.xml',
        'views/doctor_view.xml',
        'views/department_view.xml',
        'views/res_partner_views.xml',
        'report/patient_report.xml',
        'report/patient_template.xml',
        'report/sale_report_inherit.xml',

    ],
    # only loaded in demonstration mode
    'demo': [],
}
