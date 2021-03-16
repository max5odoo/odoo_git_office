# -*- coding: utf-8 -*-
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
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website', 'mail', 'sale', ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security_prac.xml',
        # 'data/student_data.xml',
        'views/students.xml',
        'views/professor.xml',
        # 'views/button_prac.xml',
        # 'views/sale_order_updates.xml',
        'views/task.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False
}
