{
    'name': "manthan",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '14.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website', 'mail', 'sale','hr_attendance' ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security_prac.xml',
        # 'data/student_data.xml',
        'views/professor.xml',
        'views/task.xml',
        'views/students.xml',
        'views/wizard_demo.xml'
        # 'views/button_prac.xml',
        # 'views/sale_order_updates.xml',


    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False
}
# -*- coding: utf-8 -*-
