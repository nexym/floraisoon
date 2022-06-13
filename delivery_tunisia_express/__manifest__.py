# -*- coding: utf-8 -*-
{
    'name': "delivery_tunisia_express",

    'summary': """
        An module for external connectivity between tunisia express shipment organization software with odoo for online shipment orders and tracking""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Nazir Khan Wazir",
    'website': "https://nazirkhanwazir.odoo.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'external',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'stock', 'delivery'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/delivery_tunisia_data.xml',
        'views/delivery_tunisia_views.xml',
        'views/delivery_carrier_inherit.xml',
        'views/sale_order_inherit.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
