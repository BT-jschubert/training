{
    'name': "Openacademy Module",
    'version': '1.0',
    'depends': ['base'],
    'author': "Carlos J. Cebrian",
    'category': 'eLearning',
    'description': "A module in wich you can learn a lot of things about openerp",
    'auto_install': False,
    'demo': ['demo/demo_data.xml'],
    'data': ['views/course_views.xml',
             'views/session_views.xml',
             'views/menu.xml',
             'views/partner_ext_views.xml',
             'wizard/wizard.xml',
             'data/session_cron.xml',
             'security/security.xml',
             'security/ir.model.access.csv',
             'reports/session_report.xml']
}