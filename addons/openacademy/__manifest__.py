{
    'name': 'OpenAcademy',
    'category': 'Academy',
    'description': """
    OpenAcademy Description
    """,
    'depends': ['base','contacts'],
    'author': 'JSchubert',
    'demo': [
        'demo/openacademy_course.xml',
        'demo/openacademy_session.xml',
    ],
    'data': [
        'security/ir.model.access.csv',

        'views/openacademy.xml',
        'views/course.xml',
        'views/session.xml',
    ],
    'license': 'OPL-1',
    'application': True,
    'without_demo': False,
}
