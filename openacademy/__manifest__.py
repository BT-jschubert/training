# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'OpenAcademy',
    'version': '1.0',
    'summary': 'First training module',
    'sequence': 30,
    'description': """

    """,
    'category': 'Training',
    'depends': [
        'base',
        'web_gantt'
    ],
    'data': [
        'data/base_data.xml',
        'data/cron.xml',
        'views/openacademy_main_view.xml',
        'views/course_view.xml',
        'views/session_view.xml',
        'views/course_ext_view.xml',
        'wizard/wizard_view.xml',

    ],
    'demo': [
        'demo/course_demo.xml'
    ],
    'qweb': [

    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
