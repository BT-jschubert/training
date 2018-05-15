{
    'name': "OPENACADEMY",
    'version': '1.0',
    'depends': ['base'],
    'author': "Javier Ortells",
    'description': """
                    My first module for Odoo, part of the Technical training
                   """,
    # data files always loaded at installation
    'data': [
        "data/schedulers.xml",
        "wizard/wizard_view.xml",
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/course_views.xml",
        "views/session_views.xml",
        "views/partner_views.xml",
        "views/menu.xml",
        "reports/session_reports.xml"
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        "demo/demo_data.xml"
    ],
    'auto_install': False # If module and all its dependencies have to be installed automatically
}
