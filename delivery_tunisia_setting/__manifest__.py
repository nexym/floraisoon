# -*- coding: utf-8 -*-
{
    'name': "delivery_tunisia_setting",

    'summary': """
        setup environment for external shipment module to install from sales or inventory settings""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Nazir Khan Wazir",
    'website': "https://nazirkhanwazir.odoo.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'External',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'stock', 'delivery'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_config_setting_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'auto_install': True,
}
