{
    'name': "Open Academy",
    'version': '1.0',
    'depends': ['base'],
    'author': "Alessandro Mascherpa",
    'category': 'training',
    'without_demo': False,
    'description': """
    Training exercise
    """
    ,
    # data files always loaded at installation
    'data': [
        'data/menu.xml',
        'data/tags.xml',
        'views/course.xml',
        'views/session.xml',
        'views/res_partner.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        'demo/course.xml',
        'demo/session.xml',
    ],
}