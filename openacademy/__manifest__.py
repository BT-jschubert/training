{
    'name': 'OpenAcademy',
    'version': '11.0.0.0.0',
    'summary': 'First training module',
    'sequence': 30,
    'author': 'brain-tec AG',
    'category': 'Training',
    'license': '',
    'depends': [
        'base',
        'web_gantt',
        'board'
    ],
    'data': [
        'data/base_data.xml',
        'reports/report_session.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
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
