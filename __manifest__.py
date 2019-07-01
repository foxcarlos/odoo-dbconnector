# -*- coding: utf-8 -*-
{
    'name': "odoo-dbconnector",

    'summary': """
        Odoo Module for store string paramaters of database engine""",

    'description': """
        Odoo Module for store string parameters of database engine. 
    """,

    'author': "foxcarlos",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '12.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/views_messagebox.xml',
        'data/dbconnector.engine.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
