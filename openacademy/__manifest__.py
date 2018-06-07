{
    'name': "OPENACADEMY",
    'version': '1.0',
    'depends': ['base'],
    'author': "MIGUEL ANGEL",
    'category': 'Category',
    'description': """
                    MODULE FROM TRAINING.
                   """,
    # data files always loaded at installation
    'data': [
        "views/courses_views.xml",
        "views/courses_menu.xml",
        "views/sessions_views.xml",
        "views/sessions_menu.xml",
        "views/partners_views.xml",
        "views/wizard_views.xml",
        "security/security.xml",
        "security/ir.model.access.csv",
        "reports/sessions_report.xml",
        "reports/qweb_session_report.xml"
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        "data/courses_demo_data.xml",
        "data/sessions_demo_data.xml"
    ],
    'auto_install': False # If module and all its dependencies have to be installed automatically
}