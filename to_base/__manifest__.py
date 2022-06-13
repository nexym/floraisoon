# -*- coding: utf-8 -*-
{
    'name': "TVTMA Base",

    'summary': """
Additional tools and utilities for other modules""",

    'description': """
Base module that provides additional tools and utilities for developers

* Check if barcode exist by passing model and barcode field name
* Generate barcode from any number
* Find the IP of the host where Odoo is running.
* Date & Time Utilities

  * Convert time to UTC
  * UTC to local time
  * Get weekdays for a given period
  * Same Weekday next week
  * Split date
* Zip a directory and return bytes object which is ready for storing in Binary fields. No on-disk temporary file is needed.
  
  * usage: zip_archive_bytes = self.env['to.base'].zip_dir(path_to_directory_to_zip)
* Sum all digits of a number (int|float)
* Finding the lucky number (digit sum = 9) which is nearest the given number
* Return remote host IP by sending http request to http(s)://base_url/my/ip/
* Replace the SQL constraint `unique_name_per_day` in res.currency.rate model with Python constraint

Editions Supported
==================
1. Community Edition
2. Enterprise Edition

    """,

    'author': "T.V.T Marine Automation (aka TVTMA),Viindoo",
    'website': 'https://viindoo.com',
    'live_test_url': 'https://v12demo-int.erponline.vn',
    'support': 'apps.support@viindoo.com',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Technical Settings',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['web', 'base_setup'],
    "assets": {
        "web.assets_backend": [
            # "/to_base/static/src/js/widgets.js",
            # "/to_base/static/src/scss/to_base.scss",
        ],
    },
    'post_load': 'post_load',
    'installable': True,
    'auto_install': True,
    'price': 9.9,
    'currency': 'EUR',
    'license': 'OPL-1',
}
