{
    'name': "Openacademy Module",
    'version': '1.0',
    'depends': ['base'],
    'author': "Carlos J. Cebrian",
    'category': 'eLearning',
    'description': "A module in wich you can learn a lot of things about openerp",
    'auto_install': False,
    'demo': ['demo/res_partner_category_demo_data.xml',
             'demo/course_demo_data.xml',
             'demo/session_demo_data.xml'
             ],
    'data': ['data/session_cron.xml',
             'views/course_views.xml',
             'views/session_views.xml',
             'views/menu.xml',
             'views/partner_ext_views.xml',
             'wizard/wizard.xml',
             'reports/session_report.xml',
             'security/security.xml',
             'security/ir.model.access.csv']
}