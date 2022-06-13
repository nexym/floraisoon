# -*- coding: utf-8 -*-

{
    'name': "Biometric Attendance Device",
    'summary': """
        Integrate all kinds of ZKTeco based attendance devices with Odoo""",
    'description': """
    """,
    'author': "T.V.T Marine Automation (aka TVTMA),Viindoo",
    'website': 'https://viindoo.com',
    'live_test_url': 'https://v12demo-int.erponline.vn',
    'support': 'apps.support@viindoo.com',
    'category': 'Human Resources',
    'version': '1.1.2',
    # any module necessary for this one to work correctly
    'depends': ['hr_attendance', 'to_base', 'to_safe_confirm_button'],
    # always loaded
    'data': [
        'data/scheduler_data.xml',
        'data/attendance_state_data.xml',
        'data/mail_template_data.xml',
        'security/module_security.xml',
        'security/ir.model.access.csv',
        'views/menu_view.xml',
        'views/attendance_device_views.xml',
        'views/attendance_state_views.xml',
        'views/device_user_views.xml',
        'views/hr_attendance_views.xml',
        'views/hr_employee_views.xml',
        'views/user_attendance_views.xml',
        'views/attendance_activity_views.xml',
        'views/finger_template_views.xml',
        'wizard/attendance_wizard.xml',
        'wizard/employee_upload_wizard.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 198.9,
    'currency': 'EUR',
    'license': 'OPL-1',
}
