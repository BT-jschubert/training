{
    'name': "Open Academy",
    'version': '1.0',
    'depends': ['base', 'board'],
    'author': "Alessandro Mascherpa",
    'category': 'training',
    'without_demo': False,
    'description': """
    Training exercise
    """
    ,
    # data files always loaded at installation
    'data': [
        'data/tags.xml',
        'data/scheduler.xml',
        'views/menu.xml',
        'views/course.xml',
        'views/session.xml',
        'views/session_board.xml',
        'views/res_partner.xml',
        'wizard/wizard_view.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'reports/session_reports.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        'demo/course.xml',
        'demo/session.xml',
    ],
}